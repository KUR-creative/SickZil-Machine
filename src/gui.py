from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QUrl
from PyQt5.QtQuick import QQuickImageProvider, QQuickItemGrabResult
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QFileDialog

from tqdm import tqdm
import utils.fp as fp
from ImListModel import ImListModel
import imgio as io
import consts
import state
import core
from pathlib import Path

def imgpath2mask(imgpath):
    return fp.go(
        imgpath,
        lambda path: io.load(path, io.NDARR),
        core.segmap,
        io.segmap2mask
    )

class ImageProvider(QQuickImageProvider):
    def __init__(self):
        super(ImageProvider, self).__init__(
            QQuickImageProvider.Image) 
    def requestImage(self, path, size):
        img = io.load(path)
        return img, img.size()

class MainWindow(QObject):
    @pyqtSlot(str, result=QVariant)
    def config(self, key):
        return consts.config[key]

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
            consts.MAIN_CONTEXT_NAME, self)
        engine.rootContext().setContextProperty(
            'ImModel', self.im_model)
        engine.addImageProvider(
            'imageUpdater', ImageProvider())
        engine.addImageProvider(
            'maskProvider', ImageProvider())

        engine.load(consts.MAIN_QML)
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

    @pyqtSlot(QUrl, result=str)
    def open_project(self, dir_url):
        dirpath = dir_url.toLocalFile()

        dir_type = state.dir_type(dirpath)
        if dir_type == consts.UNSUPPORT_DIR: 
            self.warning.emit(
                consts.WARN_MSGS[consts.UNSUPPORT_DIR])
        elif dir_type == consts.FLAT_IMGDIR:
            self.imgsToProjWarning.emit()
        else:
            self.set_project(dirpath)
            return dirpath

    @pyqtSlot(QUrl, result=str)
    def new_project(self, src_imgdir):
        '''
        create new project directory from src image directory to dst
        '''
        imgdir = src_imgdir.toLocalFile()
        p = Path(imgdir)
        default_projdir = str(
            p.with_name( consts.default_proj_name(p.name) )
        )

        projdir,_ = QFileDialog.getSaveFileName(
            caption=consts.config["new_project_dialog"]["caption"],
            directory=default_projdir,
            filter=consts.config["new_project_dialog"]["filter"]
        )

        new_projdir = state.new_project(imgdir, projdir)
        if new_projdir:
            self.set_project(new_projdir)
            return new_projdir

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
    @pyqtSlot()
    def gen_mask(self): 
        imgpath = state.now_image()
        if imgpath is None: return None

        mask = imgpath2mask(imgpath)
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
        ''' 
        Generate NEW mask of all image.
        NOTE: All previously saved masks will be overwritten.
        '''
        if state.now_image() is None: return None

        masks = fp.map(imgpath2mask, state.img_paths)

        for path,mask in tqdm(zip(state.mask_paths, masks),
                              total=len(state.img_paths),
                              desc='Generate Masks'):
            io.save(path, mask)
        self.update_gui()

        return masks

    @pyqtSlot()
    def rm_txt_all(self): 
        ''' 
        Remove text of all image.
        NOTE: If image has previously saved masks, then use it.
        '''
        if state.now_image() is None: return None

        self.saveMask.emit(state.now_mask()) # save current edited mask
        no_mask_path_pairs = fp.lremove(
            lambda pair: Path(pair.mask).exists(),
            state.img_mask_pairs()
        )
        new_masks = fp.map(
            lambda p: imgpath2mask(p.img),
            no_mask_path_pairs
        )
        for mask,pair in tqdm(zip(new_masks, no_mask_path_pairs),
                              total=len(no_mask_path_pairs),
                              desc='Generate Masks'):
            io.save(pair.mask, mask)

        img_paths,mask_paths = state.project()
        images= fp.map(lambda p: io.load(p, io.IMAGE), img_paths)
        masks = fp.map(lambda p: io.load(p, io.MASK), mask_paths)
        inpainteds = fp.map(core.inpainted, images,masks)

        for ipath,inpainted in tqdm(zip(img_paths, inpainteds),
                                    total=len(img_paths),
                                    desc='  Remove Texts'):
            io.save(ipath, inpainted) 
        self.update_gui()

    #---------------------------------------------------
    @pyqtSlot()
    def restore_prev_image(self):
        if state.now_image() is None: return None
        # TODO: It's definitely not gui functionality. 
        #       but.. where to place this function? tool.py?
        import shutil
        shutil.copy(
            state.prev_image(), state.now_image()
        )
        self.update_gui()
