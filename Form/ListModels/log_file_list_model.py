from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex

class LogFileListModel(QAbstractListModel):
    NameRole = Qt.UserRole + 1
    MacRole = Qt.UserRole + 2

    def __init__(self, items=None):
        super().__init__()
        self._items = items or []

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid():
            return None

        item = self._items[index.row()]

        if role == Qt.DisplayRole:
            return str(item)
        return None

    def rowCount(self, parent=QModelIndex()):
        return len(self._items)

    def add_item(self, item):
        self.beginInsertRows(QModelIndex(), len(self._items), len(self._items))
        self._items.append(item)
        self.endInsertRows()

    def clear(self):
        self.beginResetModel()
        self._items.clear()
        self.endResetModel()

    #----------
    def roleNames(self):
        return {
            Qt.DisplayRole: b'display',
            self.NameRole: b'file_name',
        }

    def get(self, index: QModelIndex):
        if index.isValid() and 0 <= index.row() < len(self._items):
            return self._items[index.row()]
        return None

    def remove_item(self,entity):
        for i, item in enumerate(self._items):
            if item == entity:
                self.beginRemoveRows(QModelIndex(),i,i)
                del self._items[i]
                self.endRemoveRows()
                break