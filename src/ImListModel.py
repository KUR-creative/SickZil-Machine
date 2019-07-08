from pathlib import Path
from PyQt5.QtCore import Qt, QAbstractListModel, QModelIndex # ImListModel
import utils.fp as fp
import state


class ImListModel(QAbstractListModel):
    imagePath= Qt.UserRole + 1
    maskPath = Qt.UserRole + 2
    displayed= Qt.UserRole + 3

    def __init__(self, parent=None):
        super().__init__(parent)
        self.images = ()
        self.masks = ()

    def open(self, img_paths, mask_paths):
        self.update(img_paths, mask_paths)

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
        self.images= fp.lmap(content, img_paths)
        self.masks = fp.lmap(content, mask_paths)
        self.endInsertRows() #-----------------------

    def data(self, index, role=Qt.DisplayRole):
        #print('data called! index =', index, 'role =', role)
        y = index.row()
        if role == ImListModel.imagePath:
            return self.images[y]
        if role == ImListModel.maskPath:
            return self.masks[y]
        if role == ImListModel.displayed: 
            return y == state._cursor

    def rowCount(self, parent=QModelIndex()):
        return len(self.images)

    def roleNames(self): 
        ''' specify role names in qml '''
        return {
            ImListModel.imagePath: b'image',
            ImListModel.maskPath: b'mask',
            ImListModel.displayed: b'displayed'
        }
