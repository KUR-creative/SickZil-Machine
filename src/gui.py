from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QUrl
from PyQt5.QtQuick import QQuickImageProvider
import config
import state
import utils.imutils as iu
import utils.fp as fp

def unpack_request(type_path):
    return type_path.split('?',1)

class ImageUpdater(QQuickImageProvider):
    def __init__(self):
        super(ImageUpdater, self).__init__(
            QQuickImageProvider.Image 
        ) 

    def requestImage(self, type_path, size):
        im_type,path = unpack_request(type_path)
        return fp.go(
            path,
            iu.imread,
            iu.channel3img,
            iu.nparr2qimg,
            lambda im: (im, im.size())
        )

class MainWindow(QObject):
    imageUpdate = pyqtSignal(str, arguments=['type_path']) 
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
        # get type of dirpath
        # set or.. 
        state.set_project(dirpath)
