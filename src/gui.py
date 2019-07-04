import config
import utils.imutils as iu
import utils.fp as fp
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtQuick import QQuickImageProvider

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
            config.main_qml_context, self
        )
        engine.addImageProvider(
            'imageUpdater', ImageUpdater()
        )
        engine.load(config.main_qml)

        self.window = engine.rootObjects()[0]
