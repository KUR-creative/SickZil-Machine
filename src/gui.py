from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QUrl
from PyQt5.QtQuick import QQuickImageProvider, QQuickItemGrabResult
from PyQt5.QtCore import QVariant

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
    imageUpdate = pyqtSignal(str, arguments=['path']) 
    warning = pyqtSignal(str, arguments=['msg'])
    maskProvide = pyqtSignal(str, arguments=['path']) 
    # TODO: Rename provideMask
    saveMask = pyqtSignal(str, arguments=['path'])
    rmtxtPreview = pyqtSignal()

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
            self.imageUpdate.emit(now_imgpath)
            self.maskProvide.emit(state.now_mask())
            self.im_model.update()

    #---------------------------------------------------
    @pyqtSlot(QUrl)
    def open_project(self, dir_url):
        dirpath = dir_url.toLocalFile()

        dir_type = state.dir_type(dirpath)
        if dir_type == config.UNSUPPORT_DIR: 
            self.warning.emit(
                config.WARN_MSGS[config.UNSUPPORT_DIR]
            )
            return dir_type # for test
        if dir_type == config.FLAT_IMGDIR:
            #TODO: create project directory structure
            #      and then copy images into 'images'
            #      and then reset dirpath
            #      and then below: use project directory
            self.warning.emit(
                config.WARN_MSGS[config.FLAT_IMGDIR]
            )
        else:
            state.set_project(dirpath)
            self.update_gui()

        return dir_type

    @pyqtSlot()
    def display_next(self):
        import time 
        self.saveMask.emit(state.now_mask())
        state.next()
        #time.sleep(0.2)
        self.update_gui()

    @pyqtSlot()
    def display_prev(self):
        import time 
        self.saveMask.emit(state.now_mask())
        state.prev()
        #time.sleep(0.25)
        self.update_gui()

    @pyqtSlot(int)
    def display(self, index):
        self.saveMask.emit(state.now_mask())
        state.cursor(index)
        self.update_gui()

    # NOTE: for DEBUG
    #@pyqtSlot(QObject)
    #@pyqtSlot(QMatrix)
    #@pyqtSlot(QVariantList)
    #@pyqtSlot(QVariant)
    #def get_canvas(self, data):
    @pyqtSlot(QQuickItemGrabResult)
    def get_canvas(self, img):
        import utils.imutils as iu
        import cv2
        nparr = iu.qimg2nparr(img.image())
        cv2.imshow('im',nparr); #cv2.waitKey(0)
        '''
        print(data)
        print(type(data))
        print(dir(data))
        print(data.isArray())
        print('->',data.toQObject())
        print('---')
        print(data.isArray(), 
            data.isBool(), 
            data.isCallable(), 
            data.isDate(), 
            data.isError(), 
            data.isNull(), 
            data.isNumber(), 
            data.isObject(), # <- True
            '|', data.isQObject(), data.isRegExp(), data.isString(), data.isUndefined(), data.isVariant())
        from pprint import pprint
        def dump(obj):
            for attr in dir(obj):
                print("obj.%s = %r" % (attr, getattr(obj, attr)))
        dump(data)
        '''
    #---------------------------------------------------
    @pyqtSlot()
    def gen_mask(self): 
        imgpath = state.now_image()
        if imgpath is None: return None

        mask = fp.go(
            imgpath,
            lambda path: io.load(path, io.NDARR),
            core.segmap,
            io.segmap2mask
        )
        io.save(state.now_mask(), mask)
        self.update_gui()

        return mask

    @pyqtSlot()
    def rm_txt(self):
        imgpath  = state.now_image()
        maskpath = state.now_mask()
        if imgpath is None: return None

        image = io.load(imgpath, io.IMAGE)
        mask  =(io.load(maskpath, io.MASK) 
                if Path(maskpath).exists()
                else io.mask2segmap(self.gen_mask()))
        inpainted = core.inpainted(image, mask)

        io.save(state.now_image(), inpainted)
        self.update_gui()
        self.rmtxtPreview.emit()
