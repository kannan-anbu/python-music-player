from gui.list.models import *
from config.dimention import *
from gui.list.delegates import *


class BaseList(QFrame):

    sig_onListItemSelected = pyqtSignal('QVariant', name='sig_onListItemSelected')

    def __init__(self, parent=None, geometry=PAGER_PAGE_GEO):
        super(BaseList, self).__init__(parent)
        self.initUi(geometry)

    def initUi(self, geometry):
        self.setGeometry(*geometry)
        self.setContentsMargins(
            QMargins(*PAGER_PAGE_PADDING)
        )

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.layout.setSpacing(0)

        self.listView = QListView(self)
        self.listView.setUniformItemSizes(True)
        self.listView.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.listView.setStyleSheet(
            """
            QListView {
                border: none;
                padding: 0px;
                background-color: rgba(0, 0, 0, 0);
            }
            QListView::item {
                color: black;
                padding: 4px;
                margin: 14px;
                background-color: rgba(225, 225, 255, 100);
            }
            QListView::item:hover {
                background-color: rgba(200, 200, 200, 255);
            }
            QListView::item:selected {
                color: white;
                background-color: rgba(0, 0, 0, 200);
            }
            """
        )

        self.listView.verticalScrollBar().setStyleSheet(
            """
            QScrollBar:vertical {
                background-color: #00000000;
                width: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #4fffffff;
                min-height: 20px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #afffffff;
            }
            QScrollBar::sub-line:vertical {
                height: 0px;
                width: 0px;
            }
            QScrollBar::add-line:vertical {
                height: 0px;
                width: 0px;
            }
            """
        )

        self.layout.addWidget(self.listView)
        self.setLayout(self.layout)
        self.show()

    def setdataSource(self, data, model=None, delegate=None):
        self.listModel = model
        self.listView.setModel(self.listModel)
        self.listModel.loadData(data)

        self.listView.setItemDelegate(delegate)
        self.selectionModel = self.listView.selectionModel()
        self.selectionModel.currentChanged.connect(self.onItemSelected)

    def onItemSelected(self, current, previous):
        self.sig_onListItemSelected.emit(
            current.model().data(current)
        )


class QueueList(BaseList):

    sig_onQueueSongSelected = pyqtSignal('QVariant', name='sig_onQueueSongSelected')

    def __init__(self, parent=None, geometry=PAGER_PAGE_GEO):
        super(QueueList, self).__init__(parent)

    def setdataSource(self, data, model=None, delegate=None):
        super().setdataSource(
            data,
            QueueListModel(self.listView),
            QueueListDelegate(self)
        )

    def onItemSelected(self, current, previous):
        self.sig_onQueueSongSelected.emit(
            current.model().data(current)
        )


class SongsList(BaseList):

    sig_onSongSelected = pyqtSignal('QVariant', name='sig_onSongSelected')

    def __init__(self, parent=None, geometry=PAGER_PAGE_GEO):
        super(SongsList, self).__init__(parent)

    def setdataSource(self, data, model=None, delegate=None):
        super().setdataSource(
            data,
            SongsListModel(self.listView),
            SongsListDelegate(self)
        )

    def onItemSelected(self, current, previous):
        self.sig_onSongSelected.emit(
            current.model().data(current)
        )


class AlbumsList(BaseList):

    sig_onAlbumSelected = pyqtSignal('QVariant', name='sig_onAlbumSelected')

    def __init__(self, parent=None, geometry=PAGER_PAGE_GEO):
        super(AlbumsList, self).__init__(parent)

    def setdataSource(self, data, model=None, delegate=None):
        super().setdataSource(
            data,
            AlbumsListModel(self.listView),
            AlbumsListDelegate(self)
        )

    def onItemSelected(self, current, previous):
        self.sig_onAlbumSelected.emit(
            current.model().data(current)
        )


class ArtistsList(BaseList):

    sig_onArtistSelected = pyqtSignal('QVariant', name='sig_onArtistSelected')

    def __init__(self, parent=None, geometry=PAGER_PAGE_GEO):
        super(ArtistsList, self).__init__(parent)

    def setdataSource(self, data, model=None, delegate=None):
        super().setdataSource(
            data,
            ArtistsListModel(self.listView),
            ArtistsListDelegate(self)
        )

    def onItemSelected(self, current, previous):
        self.sig_onArtistSelected.emit(
            current.model().data(current)
        )


class AlbumSongsList(BaseList):

    sig_onAlbumSongSelected = pyqtSignal('QVariant', name='sig_onAlbumSongSelected')

    def __init__(self, parent=None, geometry=PAGER_PAGE_GEO):
        super(AlbumSongsList, self).__init__(parent)

    def setdataSource(self, data, model=None, delegate=None):
        super().setdataSource(
            data,
            AlbumSongsListModel(self.listView),
            AlbumSongsListDelegate(self)
        )

    def onItemSelected(self, current, previous):
        self.sig_onAlbumSongSelected.emit(
            current.model().data(current)
        )


class ArtistSongsList(BaseList):

    sig_onArtistSongSelected = pyqtSignal('QVariant', name='sig_onArtistSongSelected')

    def __init__(self, parent=None, geometry=PAGER_PAGE_GEO):
        super(ArtistSongsList, self).__init__(parent)

    def setdataSource(self, data, model=None, delegate=None):
        super().setdataSource(
            data,
            ArtistSongsListModel(self.listView),
            ArtistSongsListDelegate(self)
        )

    def onItemSelected(self, current, previous):
        self.sig_onArtistSongSelected.emit(
            current.model().data(current)
        )
