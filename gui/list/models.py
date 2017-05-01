from PyQt5.QtCore import *
from PyQt5.QtGui import *

from mediastore import imagestore
from utils.songattributes import *


class BaseListModel(QAbstractListModel):
    def __init__(self, parent=None):
        super(BaseListModel, self).__init__(parent)
        self._data = []

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self._data)

    def loadData(self, data):
        self._data = data

    def getData(self):
        return self._data.copy()


class QueueListModel(BaseListModel):
    def __init__(self, parent=None):
        super(QueueListModel, self).__init__(parent)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        if index.row() > len(self._data):
            return QVariant()
        if role == Qt.DisplayRole:
            return self._data[index.row()]
        if role == Qt.DecorationRole:
            return QVariant
        return QVariant()


class SongsListModel(BaseListModel):
    def __init__(self, parent=None):
        super(SongsListModel, self).__init__(parent)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        if index.row() > len(self._data):
            return QVariant()
        if role == Qt.DisplayRole:
            return self._data[index.row()]
        if role == Qt.DecorationRole:
            try:
                icon = QPixmap(imagestore.thumbnail_path(self._data[index.row()][TITLE]))
            except:
                icon = QPixmap('img/play.png')
            return icon
        return QVariant()


class AlbumsListModel(BaseListModel):
    def __init__(self, parent=None):
        super(AlbumsListModel, self).__init__(parent)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        if index.row() > len(self._data):
            return QVariant()
        if role == Qt.DisplayRole:
            return self._data[index.row()]
        if role == Qt.DecorationRole:
            try:
                icon = QPixmap(imagestore.thumbnail_path(self._data[index.row()][TITLE]))
            except:
                icon = QPixmap('img/play.png')
            return icon
        return QVariant()


class ArtistsListModel(BaseListModel):
    def __init__(self, parent=None):
        super(ArtistsListModel, self).__init__(parent)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        if index.row() > len(self._data):
            return QVariant()
        if role == Qt.DisplayRole:
            return self._data[index.row()]
        if role == Qt.DecorationRole:
            try:
                icon = QPixmap(imagestore.thumbnail_path(self._data[index.row()][TITLE]))
            except:
                icon = QPixmap('img/play.png')
            return icon
        return QVariant()


class AlbumSongsListModel(BaseListModel):
    def __init__(self, parent=None):
        super(AlbumSongsListModel, self).__init__(parent)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        if index.row() > len(self._data):
            return QVariant()
        if role == Qt.DisplayRole:
            return self._data[index.row()]
        if role == Qt.DecorationRole:
            try:
                icon = QPixmap(imagestore.thumbnail_path(self._data[index.row()][TITLE]))
            except:
                icon = QPixmap('img/play.png')
            return icon
        return QVariant()


class ArtistSongsListModel(BaseListModel):
    def __init__(self, parent=None):
        super(ArtistSongsListModel, self).__init__(parent)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        if index.row() > len(self._data):
            return QVariant()
        if role == Qt.DisplayRole:
            return self._data[index.row()]
        if role == Qt.DecorationRole:
            try:
                icon = QPixmap(imagestore.thumbnail_path(self._data[index.row()][TITLE]))
            except:
                icon = QPixmap('img/play.png')
            return icon
        return QVariant()
