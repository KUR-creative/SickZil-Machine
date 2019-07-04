from PyQt5.QtCore import QObject

class MainWindow(QObject):
    def __init__(self,engine):
        QObject.__init__(self)

        engine.rootContext() \
              .setContextProperty('main', self)
        engine.load('../qml/szmc-0.1.0.qml')

        self.window = engine.rootObjects()[0]
