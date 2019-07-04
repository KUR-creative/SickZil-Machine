import config
from PyQt5.QtCore import QObject

class MainWindow(QObject):
    def __init__(self,engine):
        QObject.__init__(self)

        engine.rootContext().setContextProperty(
            config.main_qml_context, self
        )
        engine.load(config.main_qml)

        self.window = engine.rootObjects()[0]
