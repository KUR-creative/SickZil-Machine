from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QUrl
from PyQt5.QtQuick import QQuickImageProvider, QQuickItemGrabResult
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QFileDialog

import utils.fp as fp
from ImListModel import ImListModel
import imgio as io
import config
import state
import core
from pathlib import Path

class ImageProvider(QQuickImageProvider):
    def __init__(self):
        super(ImageProvider, self).__init__(
            QQuickImageProvider.Image) 
    def requestImage(self, path, size):
        img = io.load(path)
        return img, img.size()

class MainWindow(QObject):
    warning     = pyqtSignal(str, arguments=['msg'])
    imgsToProjWarning = pyqtSignal()
    initialize  = pyqtSignal()
    updateImage = pyqtSignal(str, arguments=['path']) 
    provideMask = pyqtSignal(str, arguments=['path']) 
    saveMask    = pyqtSignal(str, arguments=['path'])

    def __init__(self,engine):
        QObject.__init__(self)

        self.im_model = ImListModel()
        engine.rootContext().setContextProperty(
            config.MAIN_CONTEXT_NAME, self)
        engine.rootContext().setContextProperty(
            'ImModel', self.im_model)
        engine.addImageProvider(
            'imageUpdater', ImageProvider())
        engine.addImageProvider(
            'maskProvider', ImageProvider())

        engine.load(config.MAIN_QML)
        self.window = engine.rootObjects()[0]

    def update_gui(self):
        now_imgpath = state.now_image()
        if now_imgpath:
            self.updateImage.emit(now_imgpath)
            self.provideMask.emit(state.now_mask())
            self.im_model.update()

    #---------------------------------------------------
    def set_project(self, dirpath):
        self.initialize.emit()
        state.set_project(dirpath)
        self.update_gui()

    @pyqtSlot(QUrl)
    def open_project(self, dir_url):
        dirpath = dir_url.toLocalFile()

        dir_type = state.dir_type(dirpath)
        print(dir_type)
        if dir_type == config.UNSUPPORT_DIR: 
            self.warning.emit(
                config.WARN_MSGS[config.UNSUPPORT_DIR])
        elif dir_type == config.FLAT_IMGDIR:
            self.imgsToProjWarning.emit()
        else:
            self.set_project(dirpath)
        return dir_type

    @pyqtSlot(QUrl)
    def new_project(self, src_imgdir):
        '''
        create new project directory from src image directory to dst
        '''
        imgdir = src_imgdir.toLocalFile()
        p = Path(imgdir)
        default_projdir = str(
            p.with_name( config.default_proj_name(p.name) )
        )

        projdir,_ = QFileDialog.getSaveFileName(
            caption="Create New Manga Project Folder", 
            directory=default_projdir
        )

        new_projdir = state.new_project(imgdir, projdir)
        self.set_project(new_projdir)

    #---------------------------------------------------
    @pyqtSlot()
    def display_next(self):
        import time 
        self.saveMask.emit(state.now_mask())
        state.next()
        self.update_gui()

    @pyqtSlot()
    def display_prev(self):
        import time 
        self.saveMask.emit(state.now_mask())
        state.prev()
        self.update_gui()

    @pyqtSlot(int)
    def display(self, index):
        self.saveMask.emit(state.now_mask())
        state.cursor(index)
        self.update_gui()

    # NOTE: for DEBUG
    '''
    @pyqtSlot(QQuickItemGrabResult)
    def get_canvas(self, img):
        import utils.imutils as iu
        import cv2
        nparr = iu.qimg2nparr(img.image())
        cv2.imshow('im',nparr); 
    '''
    #---------------------------------------------------
    def imgpath2mask(self, imgpath):
        return fp.go(
            imgpath,
            lambda path: io.load(path, io.NDARR),
            core.segmap,
            io.segmap2mask
        )

    @pyqtSlot()
    def gen_mask(self): 
        imgpath = state.now_image()
        if imgpath is None: return None

        mask = self.imgpath2mask(imgpath)
        io.save(state.now_mask(), mask)
        self.update_gui()

        return mask

    @pyqtSlot()
    def rm_txt(self):
        imgpath  = state.now_image()
        maskpath = state.now_mask()
        if imgpath is None: return None

        self.saveMask.emit(maskpath) # save edited mask
        image = io.load(imgpath, io.IMAGE)
        mask  =(io.load(maskpath, io.MASK) 
                if Path(maskpath).exists()
                else io.mask2segmap(self.gen_mask()))
        inpainted = core.inpainted(image, mask)

        io.save(state.now_image(), inpainted) 
        self.update_gui()

    @pyqtSlot()
    def gen_mask_all(self): 
        if state.now_image() is None: return None

        self.warning.emit(
            config.WARN_MSGS[config.MASK_ALL])

        masks = fp.lmap(self.imgpath2mask, state.img_paths)

        for path,mask in zip(state.mask_paths,masks):
            io.save(path, mask)
        self.update_gui()

        return masks

    @pyqtSlot()
    def rm_txt_all(self): 
        self.warning.emit(
            config.WARN_MSGS[config.RMTXT_ALL])
