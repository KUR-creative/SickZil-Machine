from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QUrl
from PyQt5.QtQuick import QQuickImageProvider
import config
import state
from ImListModel import ImListModel#, update_im_model
import utils.imutils as iu
import utils.futils as fu
import utils.fp as fp

class ImageUpdater(QQuickImageProvider):
    def __init__(self):
        super(ImageUpdater, self).__init__(
            QQuickImageProvider.Image 
        ) 

    def requestImage(self, path, size):
        return fp.go(
            path,
            iu.imread,
            iu.channel3img,
            iu.nparr2qimg,
            lambda im: (im, im.size())
        )

class MainWindow(QObject):
    imageUpdate = pyqtSignal(str, arguments=['path']) 
    warning = pyqtSignal(str, arguments=['msg'])

    def __init__(self,engine):
        QObject.__init__(self)

        engine.rootContext().setContextProperty(
            config.MAIN_CONTEXT_NAME, self
        )
        engine.addImageProvider(
            'imageUpdater', ImageUpdater()
        )

        self.im_model = ImListModel()
        engine.rootContext().setContextProperty(
            'ImModel', self.im_model
        )

        engine.load(config.MAIN_QML)
        self.window = engine.rootObjects()[0]

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
            # Update gui
            self.imageUpdate.emit(state.now_image())
            self.im_model.open(*state.project())

        return dir_type # for test

    @pyqtSlot()
    def next_image(self):
        state.next_image()
        self.imageUpdate.emit(state.now_image())
        self.im_model.update()

    @pyqtSlot()
    def prev_image(self):
        state.prev_image()
        self.imageUpdate.emit(state.now_image())
        self.im_model.update()

