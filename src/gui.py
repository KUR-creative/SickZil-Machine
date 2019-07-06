from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QUrl
from PyQt5.QtQuick import QQuickImageProvider
import config
import state
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
        elif dir_type == config.FLAT_IMGDIR:
            #TODO: create project directory structure
            #      and then copy images into 'images'
            #      and then reset dirpath
            #      and then below: use project directory
            self.warning.emit(
                config.WARN_MSGS[config.FLAT_IMGDIR]
            )
        else:
            state.set_project(dirpath)
            print(state.img_paths)
            print(state.mask_paths)
            self.imageUpdate.emit(state.now_image())

        return dir_type # for test
