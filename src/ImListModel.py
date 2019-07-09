# Remove self.state or not..?
from pathlib import Path
from PyQt5.QtCore import Qt, QAbstractListModel, QModelIndex # ImListModel
import utils.fp as fp
import state


class ImListModel(QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.images = ()
        self.masks = ()

    def update(self, img_paths=None, mask_paths=None):
        if (img_paths is None and mask_paths is None):
            img_paths, mask_paths = state.project()

        self.beginRemoveRows(#-----------------------
            QModelIndex(), 0, len(self.images) - 1)
        self.endRemoveRows() #-----------------------

        self.beginInsertRows(#-----------------------
            QModelIndex(), 0, len(img_paths) - 1)
        def content(path):
            p = Path(path)
            return str(Path( p.parent.name, p.name ))
        self.images= fp.lmap(content, img_paths)  # SET STATE!
        self.masks = fp.lmap(content, mask_paths) # SET STATE!
        self.endInsertRows() #-----------------------

    imagePath = Qt.UserRole + 1
    maskPath  = Qt.UserRole + 2
    displayed = Qt.UserRole + 3
    def data(self, index, role=Qt.DisplayRole):
        y = index.row()
        return {
            self.imagePath: self.images[y],
            self.maskPath : self.masks[y],
            self.displayed: y == state.cursor()
        }[role]

    def rowCount(self, parent=QModelIndex()):
        return len(self.images)

    def roleNames(self): 
        ''' specify role names in qml '''
        return {
            self.imagePath: b'image',
            self.maskPath : b'mask',
            self.displayed: b'displayed'
        }
