from gui.list.lists import *
from mediastore.musicstore import MusicStore
from gui.buttons import *


class ControlsBar(QFrame):
    def __init__(self, parent=None, geometry=CONTROLS_BAR_GEO):
        super(ControlsBar, self).__init__(parent)
        self.setParent(parent)
        self.initUi(geometry)
        self.clearUi()

    def initUi(self, geometry):
        self.setGeometry(*geometry)
        self.setObjectName('ControlsBar')
        self.setContentsMargins(
            QMargins(*CONTROLS_BAR_PADDING)
        )

        self.labelSongTitle = QLabel(self)
        self.labelSongTitle.setFixedWidth(CONTROLS_BAR_TEXT_LAYOUT_GEO[2])
        f = QFont()
        f.setPixelSize(15)
        self.labelSongTitle.setFont(f)

        self.labelSongArtist = QLabel(self)
        self.labelSongArtist.setFixedWidth(CONTROLS_BAR_TEXT_LAYOUT_GEO[2])

        self.songSlider = QSlider(self)
        self.songSlider.setOrientation(Qt.Horizontal)
        self.songSlider.setMinimum(0)
        self.songSlider.setMaximum(1000)
        self.songSlider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.labelTimeElapsed = QLabel(self)
        self.labelTimeTotal = QLabel(self)

        self.buttonLoop = LoopButton(parent=self, geometry=CONTROLS_BAR_BUTTON_SMALL_GEO)
        self.buttonPrev = PrevButton(parent=self, geometry=CONTROLS_BAR_BUTTON_SMALL_GEO)
        self.buttonPlay = PlayPauseButton(parent=self, geometry=CONTROLS_BAR_BUTTON_LARGE_GEO)
        self.buttonNext = NextButton(parent=self, geometry=CONTROLS_BAR_BUTTON_SMALL_GEO)
        self.buttonShuffle = ShuffleButton(parent=self, geometry=CONTROLS_BAR_BUTTON_SMALL_GEO)

        layoutText = QVBoxLayout()
        layoutText.setContentsMargins(
            QMargins(5, 5, 5, 5)
        )
        layoutText.addWidget(self.labelSongTitle)
        layoutText.addWidget(self.labelSongArtist)

        layoutSlider = QHBoxLayout()
        layoutSlider.addWidget(self.labelTimeElapsed)
        layoutSlider.addWidget(self.songSlider)
        layoutSlider.addWidget(self.labelTimeTotal)

        layoutButtons = QHBoxLayout()
        layoutButtons.setSpacing(CONTROLS_BAR_SPACING)
        layoutButtons.addWidget(self.buttonLoop)
        layoutButtons.addWidget(self.buttonPrev)
        layoutButtons.addWidget(self.buttonPlay)
        layoutButtons.addWidget(self.buttonNext)
        layoutButtons.addWidget(self.buttonShuffle)

        layoutMain = QHBoxLayout(self)
        layoutMain.setContentsMargins(QMargins(*NO_MARGIN))
        layoutMain.setSpacing(2 * CONTROLS_BAR_SPACING)
        layoutMain.addLayout(layoutText)
        layoutMain.addLayout(layoutSlider)
        layoutMain.addLayout(layoutButtons)

        self.setLayout(layoutMain)
        self.show()

    def setTitle(self, title):
        metrics = QFontMetrics(self.labelSongTitle.font())
        elidedTitle = metrics.elidedText(title, Qt.ElideRight, self.labelSongTitle.width())
        self.labelSongTitle.setText(elidedTitle)

    def setArtist(self, artist):
        metrics = QFontMetrics(self.labelSongArtist.font())
        elidedArtist = metrics.elidedText(artist, Qt.ElideRight, self.labelSongArtist.width())
        self.labelSongArtist.setText(elidedArtist)

    def clearUi(self):
        self.songSlider.setValue(0)
        self.setTitle('Song')
        self.setArtist('Artist')
        self.labelTimeElapsed.setText('0:00')
        self.labelTimeTotal.setText('0:00')


class NavigationBar(QFrame):
    def __init__(self, parent=None, geometry=NAV_BAR_GEO):
        super(NavigationBar, self).__init__(parent)
        self.initUi(geometry)

    def initUi(self, geometry):
        self.setGeometry(*geometry)
        self.setObjectName('NavigationBar')
        self.setContentsMargins(
            QMargins(*NAV_BAR_PADDING)
        )

        self.buttonPlayList = NavButton(parent=self, geometry=NAV_BAR_BUTTON_GEO)
        self.buttonPlayList.setIcon(QPixmap('img/grid.png'))
        self.buttonSongs = NavButton(parent=self, geometry=NAV_BAR_BUTTON_GEO)
        self.buttonSongs.setIcon(QPixmap('img/music.png'))
        self.buttonArtists = NavButton(parent=self, geometry=NAV_BAR_BUTTON_GEO)
        self.buttonArtists.setIcon(QPixmap('img/artist.png'))
        self.buttonAlbums = NavButton(parent=self, geometry=NAV_BAR_BUTTON_GEO)
        self.buttonAlbums.setIcon(QPixmap('img/album.png'))
        self.buttonQueue = NavButton(parent=self, geometry=NAV_BAR_BUTTON_GEO)
        self.buttonQueue.setIcon(QPixmap('img/sort.png'))

        layoutMain = QVBoxLayout()
        layoutMain.setContentsMargins(QMargins(*NO_MARGIN))
        layoutMain.setSpacing(NAV_BAR_SPACING)

        layoutMain.addWidget(self.buttonQueue)
        layoutMain.addWidget(self.buttonSongs)
        layoutMain.addWidget(self.buttonAlbums)
        layoutMain.addWidget(self.buttonArtists)
        layoutMain.addWidget(self.buttonPlayList)
        layoutMain.addStretch(1)

        self.setLayout(layoutMain)
        self.show()


class SongDetailsFrame(QFrame):
    def __init__(self, parent=None, geometry=SONG_DETAILS_PANEL_GEO):
        super(SongDetailsFrame, self).__init__(parent)
        self.initUi(geometry)
        self.clearUi()

    def initUi(self, geometry):
        self.setGeometry(*geometry)
        self.setObjectName('SongDetailsFrame')
        self.setContentsMargins(QMargins(*SONG_DETAILS_PANEL_PADDING))

        self.layoutSongDetails = QVBoxLayout()
        self.layoutSongDetails.setContentsMargins(QMargins(*NO_MARGIN))
        self.layoutSongDetails.setSpacing(SONG_DETAILS_PANEL_SPACING)

        self.albumArt = ImageView(self, geometry=(0, 0, 250, 250))
        self.labelSongTitle = QLabel(self)
        self.labelSongTitle.setMinimumWidth(
            geometry[2] // 10 * 8
        )
        self.labelSongTitle.setMaximumWidth(
            geometry[2] // 10 * 8
        )
        f = QFont()
        f.setPixelSize(17)
        self.labelSongTitle.setFont(f)
        self.labelSongAlbum = QLabel(self)
        self.labelSongAlbum.setMaximumWidth(
            geometry[2] // 10 * 8
        )
        f = QFont()
        f.setPixelSize(14)
        self.labelSongAlbum.setFont(f)
        self.labelSongArtist = QLabel(self)
        self.labelSongArtist.setMaximumWidth(
            geometry[2] // 10 * 8
        )
        f = QFont()
        f.setPixelSize(12)
        self.labelSongArtist.setFont(f)

        self.labelTitle1 = QLabel('Song')
        self.labelTitle1.setObjectName('Dull')
        self.labelTitle2 = QLabel('Album')
        self.labelTitle2.setObjectName('Dull')
        self.labelTitle3 = QLabel('Artist')
        self.labelTitle3.setObjectName('Dull')

        self.layoutSongDetails.addWidget(self.albumArt)
        self.layoutSongDetails.setAlignment(self.albumArt, Qt.AlignLeft | Qt.AlignTop)
        self.layoutSongDetails.addSpacing(20)

        self.layoutSongDetails.addWidget(self.labelTitle1)
        self.layoutSongDetails.addWidget(self.labelSongTitle)
        self.layoutSongDetails.addSpacing(10)
        self.layoutSongDetails.addWidget(self.labelTitle2)
        self.layoutSongDetails.addWidget(self.labelSongAlbum)
        self.layoutSongDetails.addSpacing(10)
        self.layoutSongDetails.addWidget(self.labelTitle3)
        self.layoutSongDetails.addWidget(self.labelSongArtist)
        self.layoutSongDetails.addStretch(1)

        self.setLayout(self.layoutSongDetails)
        self.show()

    def updateUi(self, song):
        albumartPixmap = QPixmap(imagestore.albumart_path(song[TITLE]))
        self.albumArt.setImage(albumartPixmap)

        title = song[TITLE]
        elidedTitle = self.labelSongTitle.fontMetrics().elidedText(title, Qt.ElideRight, self.labelSongTitle.width())
        self.labelSongTitle.setText(elidedTitle)

        album = song[ALBUM]
        elidedAlbum = self.labelSongAlbum.fontMetrics().elidedText(album, Qt.ElideRight, self.labelSongAlbum.width())
        self.labelSongAlbum.setText(elidedAlbum)

        artist = song[ARTIST]
        elidedArtist = self.labelSongArtist.fontMetrics().elidedText(artist, Qt.ElideRight, self.labelSongArtist.width())
        self.labelSongArtist.setText(elidedArtist)

    def clearUi(self):
        albumartPixmap = QPixmap(imagestore.albumart_path('^%&^%&'))
        self.albumArt.setImage(albumartPixmap)
        self.labelSongTitle.setText('')
        self.labelSongAlbum.setText('')
        self.labelSongArtist.setText('')


class SongQueueFrame(QFrame):
    def __init__(self, parent=None, geometry=SONG_DETAILS_PANEL_GEO):
        super(SongQueueFrame, self).__init__(parent)
        self.initUi(geometry)

    def initUi(self, geometry):
        self.setGeometry(*geometry)
        self.setObjectName('SongQueueFrame')
        self.setContentsMargins(QMargins(*SONG_DETAILS_PANEL_PADDING))

        self.layoutMain = QVBoxLayout()
        self.layoutMain.setContentsMargins(QMargins(*NO_MARGIN))
        self.layoutMain.setSpacing(PAGER_PAGE_SPACING)

        self.layoutHeader = QHBoxLayout()
        self.layoutMain.setContentsMargins(QMargins(*NO_MARGIN))
        self.layoutMain.setSpacing(PAGER_PAGE_SPACING)

        self.labelTitle = QLabel(self)
        f = QFont()
        f.setPixelSize(17)
        self.labelTitle.setFont(f)
        self.labelTitle.setText('Queued Songs')

        self.clearButton = NavButton(self, geometry=(0, 0, 30, 30))
        self.clearButton.setIcon(QPixmap('img/clear.png'))

        self.layoutHeader.addWidget(self.labelTitle)
        self.layoutHeader.addStretch(1)
        self.layoutHeader.addWidget(self.clearButton)

        self.listQueue = QueueList(self, geometry=NOW_PLAYING_QUEUE_GEO)

        self.layoutMain.addLayout(self.layoutHeader)
        self.layoutMain.addWidget(self.listQueue)

        self.setLayout(self.layoutMain)
        self.show()


class NowPlayingPage(QFrame):
    def __init__(self, parent=None, geometry=PAGER_PAGE_GEO):
        super(NowPlayingPage, self).__init__(parent)
        self.initUi(geometry)

    def initUi(self, geometry):
        self.setGeometry(*geometry)
        self.setObjectName('NowPlayingPage')
        self.setContentsMargins(QMargins(*PAGER_PAGE_PADDING))

        self.layoutMain = QHBoxLayout()
        self.layoutMain.setContentsMargins(QMargins(*NO_MARGIN))
        self.layoutMain.setSpacing(2*PAGER_PAGE_SPACING)

        self.songDetailsFrame = SongDetailsFrame(self, geometry=SONG_DETAILS_PANEL_GEO)
        self.songQueueFrame = SongQueueFrame(self, geometry=SONG_DETAILS_PANEL_GEO)

        self.layoutMain.addWidget(self.songDetailsFrame)
        self.layoutMain.addWidget(self.songQueueFrame)

        self.setLayout(self.layoutMain)
        self.show()

    def updateUi(self, song):
        self.songDetailsFrame.updateUi(song)


class AlbumDetailsFrame(QFrame):

    def __init__(self, parent=None, geometry=PAGER_PAGE_GEO):
        super(AlbumDetailsFrame, self).__init__(parent)
        self.initUi(geometry)

    def initUi(self, geometry):
        self.setGeometry(*geometry)
        self.setObjectName('AlbumsPage')
        self.setContentsMargins(QMargins(*PAGER_PAGE_PADDING))

        self.layoutMain = QVBoxLayout()
        self.layoutMain.setContentsMargins(
            QMargins(*NO_MARGIN)
        )
        self.layoutMain.setSpacing(PAGER_PAGE_SPACING)

        self.layoutHeader = QHBoxLayout()
        self.layoutHeader.setContentsMargins(
            QMargins(*NO_MARGIN)
        )
        self.layoutHeader.setSpacing(PAGER_HEADER_SPACING)

        self.closeButton = NavButton(self, geometry=(0, 0, 40, 40))
        self.closeButton.setIcon(QPixmap('img/back.png'))

        self.albumArt = ImageView(self, geometry=(0, 0, 200, 200))
        self.labelAlbumTitle = QLabel(self)
        self.labelAlbumTitle.setMinimumWidth(
            geometry[2] - 200
        )
        f = QFont()
        f.setPixelSize(17)
        self.labelAlbumTitle.setFont(f)
        self.labelAlbumYear = QLabel(self)
        f = QFont()
        f.setPixelSize(14)
        self.labelAlbumYear.setFont(f)
        self.labelAlbumSongCount = QLabel(self)
        f = QFont()
        f.setPixelSize(12)
        self.labelAlbumSongCount.setFont(f)

        self.buttonPlayAlbum = TransparentTextButton(self, geometry=(0, 0, 150, 30))
        self.buttonPlayAlbum.setText('Play Album')

        self.buttonShuffleAlbum = TransparentTextButton(self, geometry=(0, 0, 150, 30))
        f = QFont()
        f.setPixelSize(15)
        self.buttonShuffleAlbum.setFont(f)
        self.buttonShuffleAlbum.setText('Shuffle Album')
        self.layoutRight = QVBoxLayout()

        self.layoutRight.setContentsMargins(
            QMargins(30, 10, 10, 10)
        )
        self.layoutRight.setSpacing(PAGER_HEADER_SPACING)

        self.layoutRight.addWidget(self.labelAlbumTitle)
        self.layoutRight.addWidget(self.labelAlbumYear)
        self.layoutRight.addWidget(self.labelAlbumSongCount)
        self.layoutRight.addStretch(1)
        self.layoutRight.addWidget(self.buttonPlayAlbum)
        self.layoutRight.setAlignment(self.buttonPlayAlbum, Qt.AlignLeft)
        self.layoutRight.addWidget(self.buttonShuffleAlbum)
        self.layoutRight.setAlignment(self.buttonShuffleAlbum, Qt.AlignLeft)

        self.layoutHeader.addWidget(self.closeButton)
        self.layoutHeader.setAlignment(self.closeButton, Qt.AlignTop)
        self.layoutHeader.addWidget(self.albumArt)
        self.layoutHeader.addLayout(self.layoutRight)
        self.layoutHeader.addStretch(1)

        self.albumSongList = AlbumSongsList(self)
        self.layoutMain.addLayout(self.layoutHeader)
        self.layoutMain.addWidget(self.albumSongList)

        self.setLayout(self.layoutMain)
        self.show()

    def loadData(self, songs):
        self.albumSongList.setdataSource(songs)
        albumartPixmap = QPixmap(imagestore.albumart_path(songs[0][TITLE]))
        self.albumArt.setImage(albumartPixmap)

        title = songs[0][ALBUM]
        elidedTitle = self.labelAlbumTitle.fontMetrics().elidedText(title, Qt.ElideRight, self.labelAlbumTitle.width())
        self.labelAlbumTitle.setText(elidedTitle)

        self.labelAlbumYear.setText(songs[0][YEAR])

        songCount = len(songs)
        self.labelAlbumSongCount.setText(str(songCount) + (' tracks' if songCount > 1 else ' track'))


class AlbumsPage(QFrame):

    sig_onPlayAlbum = pyqtSignal('QVariant', name='sig_onPlayAlbum')
    sig_onShuffleAlbum = pyqtSignal('QVariant', name='sig_onShuffleAlbum')
    sig_onPlaySong = pyqtSignal('QVariant', name='sig_onPlaySong')

    def __init__(self, parent=None, geometry=PAGER_PAGE_GEO):
        super(AlbumsPage, self).__init__(parent)
        self.initUi(geometry)

    def initUi(self, geometry):
        self.setGeometry(*geometry)
        self.setObjectName('AlbumsPage')
        self.setContentsMargins(QMargins(*PAGER_PAGE_PADDING))

        self.layoutMain = QHBoxLayout()
        self.layoutMain.setContentsMargins(
            QMargins(*NO_MARGIN)
        )
        self.layoutMain.setSpacing(PAGER_HEADER_SPACING)

        self.pager = Pager(self, geometry=geometry)
        self.pager.header.hide()

        self.listAlbums = AlbumsList(self, geometry=PAGER_PAGE_GEO)
        self.listAlbums.sig_onAlbumSelected.connect(self.onAlbumSelected)

        self.pager.addPage(
            {
                'id'        : 'albums list',
                'widget'    : self.listAlbums,
                'title1'    : 'Albums',
                'title2'    : 'title2',
            }
        )

        self.layoutMain.addWidget(self.pager)
        self.setLayout(self.layoutMain)
        self.show()

    def onAlbumSelected(self, album):
        self.albumDetailsFrame = AlbumDetailsFrame(self, geometry=PAGER_PAGE_GEO)
        ms = MusicStore()
        ms.init()
        self.albumDetailsFrame.loadData(ms.getSongsForAlbum(album[ALBUM]))
        ms.close()
        self.pager.addPage(
            {
                'id'        : album[ALBUM],
                'widget'    : self.albumDetailsFrame,
                'title1'    : album[ALBUM],
                'title2'    : 'title2',
            }
        )
        self.albumDetailsFrame.closeButton.sig_clicked.connect(self.onCloseAlbum)
        self.albumDetailsFrame.buttonPlayAlbum.sig_clicked.connect(self.onPlayAlbum)
        self.albumDetailsFrame.buttonShuffleAlbum.sig_clicked.connect(self.onShuffleAlbum)
        self.albumDetailsFrame.albumSongList.sig_onAlbumSongSelected.connect(self.onPlaySong)

    def onPlaySong(self, song):
        self.sig_onPlaySong.emit(song)

    def onPlayAlbum(self):
        songs = self.albumDetailsFrame.albumSongList.listModel.getData()
        self.sig_onPlayAlbum.emit(songs)

    def onShuffleAlbum(self):
        songs = self.albumDetailsFrame.albumSongList.listModel.getData()
        self.sig_onShuffleAlbum.emit(songs)

    def onCloseAlbum(self):
        self.pager.removePage()


class ArtistDetailsFrame(QFrame):

    def __init__(self, parent=None, geometry=PAGER_PAGE_GEO):
        super(ArtistDetailsFrame, self).__init__(parent)
        self.initUi(geometry)

    def initUi(self, geometry):
        self.setGeometry(*geometry)
        self.setObjectName('ArtistPage')
        self.setContentsMargins(QMargins(*PAGER_PAGE_PADDING))

        self.layoutMain = QVBoxLayout()
        self.layoutMain.setContentsMargins(
            QMargins(*NO_MARGIN)
        )
        self.layoutMain.setSpacing(PAGER_PAGE_SPACING)

        self.layoutHeader = QHBoxLayout()
        self.layoutHeader.setContentsMargins(
            QMargins(*NO_MARGIN)
        )
        self.layoutHeader.setSpacing(PAGER_HEADER_SPACING)

        self.layoutRight = QVBoxLayout()
        self.layoutRight.setContentsMargins(
            QMargins(*NO_MARGIN)
        )
        self.layoutRight.setSpacing(PAGER_HEADER_SPACING)

        self.closeButton = NavButton(self, geometry=(0, 0, 40, 40))
        self.closeButton.setIcon(QPixmap('img/back.png'))

        self.labelArtistTitle = QLabel(self)
        self.labelArtistTitle.setMinimumWidth(
            geometry[2] - 200
        )
        f = QFont()
        f.setPixelSize(17)
        self.labelArtistTitle.setFont(f)
        self.labelArtistSongCount = QLabel(self)
        f = QFont()
        f.setPixelSize(12)
        self.labelArtistSongCount.setFont(f)

        self.buttonPlayAll = TransparentTextButton(self, geometry=(0, 0, 150, 30))
        f = QFont()
        f.setPixelSize(15)
        self.buttonPlayAll.setFont(f)
        self.buttonPlayAll.setText('Play All')

        self.buttonShuffleAll = TransparentTextButton(self, geometry=(0, 0, 150, 30))
        self.buttonShuffleAll.setText('Shuffle All')

        self.layoutButtons = QHBoxLayout()

        self.layoutButtons.setContentsMargins(
            QMargins(*NO_MARGIN)
        )
        self.layoutButtons.setSpacing(PAGER_HEADER_SPACING)

        self.layoutButtons.addWidget(self.buttonPlayAll)
        self.layoutButtons.addWidget(self.buttonShuffleAll)
        self.layoutButtons.addStretch(1)

        self.layoutRight.addWidget(self.labelArtistTitle)
        self.layoutRight.addWidget(self.labelArtistSongCount)
        self.layoutRight.addLayout(self.layoutButtons)
        self.layoutRight.setAlignment(self.layoutButtons, Qt.AlignLeft)
        self.layoutHeader.addWidget(self.closeButton)
        self.layoutHeader.setAlignment(self.closeButton, Qt.AlignTop)
        self.layoutHeader.addLayout(self.layoutRight)

        self.artistSongList = ArtistSongsList(self)
        self.layoutMain.addLayout(self.layoutHeader)
        self.layoutMain.addWidget(self.artistSongList)

        self.setLayout(self.layoutMain)
        self.show()

    def loadData(self, songs):
        self.artistSongList.setdataSource(songs)

        title = songs[0][ARTIST]
        elidedTitle = self.labelArtistTitle.fontMetrics().elidedText(title, Qt.ElideRight, self.labelArtistTitle.width())
        self.labelArtistTitle.setText(elidedTitle)

        songCount = len(songs)
        self.labelArtistSongCount.setText(str(songCount) + (' tracks' if songCount > 1 else ' track'))


class ArtistsPage(QFrame):

    sig_onPlayArtist = pyqtSignal('QVariant', name='sig_onPlayArtist')
    sig_onShuffleArtist = pyqtSignal('QVariant', name='sig_onShuffleArtist')
    sig_onPlaySong = pyqtSignal('QVariant', name='sig_onPlaySong')

    def __init__(self, parent=None, geometry=PAGER_PAGE_GEO):
        super(ArtistsPage, self).__init__(parent)
        self.initUi(geometry)

    def initUi(self, geometry):
        self.setGeometry(*geometry)
        self.setObjectName('AlbumsPage')
        self.setContentsMargins(QMargins(*PAGER_PAGE_PADDING))

        self.layoutMain = QHBoxLayout()
        self.layoutMain.setContentsMargins(
            QMargins(*NO_MARGIN)
        )
        self.layoutMain.setSpacing(PAGER_HEADER_SPACING)

        self.pager = Pager(self, geometry=geometry)
        self.pager.header.hide()

        self.listArtists = ArtistsList(self, geometry=PAGER_PAGE_GEO)
        self.listArtists.sig_onArtistSelected.connect(self.onArtistSelected)

        self.pager.addPage(
            {
                'id'        : 'artists list',
                'widget'    : self.listArtists,
                'title1'    : 'Artists',
                'title2'    : 'title2',
            }
        )

        self.layoutMain.addWidget(self.pager)
        self.setLayout(self.layoutMain)
        self.show()

    def onArtistSelected(self, artist):
        self.artistDetailsFrame = ArtistDetailsFrame(self, geometry=PAGER_PAGE_GEO)
        ms = MusicStore()
        ms.init()
        self.artistDetailsFrame.loadData(ms.getSongsForArtist(artist[ARTIST]))
        ms.close()
        self.pager.addPage(
            {
                'id'        : artist[ARTIST],
                'widget'    : self.artistDetailsFrame,
                'title1'    : artist[ARTIST],
                'title2'    : 'title2',
            }
        )
        self.artistDetailsFrame.closeButton.sig_clicked.connect(self.onCloseArtist)
        self.artistDetailsFrame.buttonPlayAll.sig_clicked.connect(self.onPlayArtist)
        self.artistDetailsFrame.buttonShuffleAll.sig_clicked.connect(self.onShuffleArtist)
        self.artistDetailsFrame.artistSongList.sig_onArtistSongSelected.connect(self.onPlaySong)

    def onPlaySong(self, song):
        self.sig_onPlaySong.emit(song)

    def onPlayArtist(self):
        songs = self.artistDetailsFrame.artistSongList.listModel.getData()
        self.sig_onPlayArtist.emit(songs)

    def onShuffleArtist(self):
        songs = self.artistDetailsFrame.artistSongList.listModel.getData()
        self.sig_onShuffleArtist.emit(songs)

    def onCloseArtist(self):
        self.pager.removePage()


class SongsPage(QFrame):

    sig_onPlayAll = pyqtSignal('QVariant', name='sig_onPlayArtist')
    sig_onShuffleAll = pyqtSignal('QVariant', name='sig_onShuffleArtist')
    sig_onPlaySong = pyqtSignal('QVariant', name='sig_onPlaySong')

    def __init__(self, parent=None, geometry=PAGER_PAGE_GEO):
        super(SongsPage, self).__init__(parent)
        self.initUi(geometry)
        self.setupEvents()

    def initUi(self, geometry):
        self.setGeometry(*geometry)
        self.setObjectName('SongsPage')
        self.setContentsMargins(QMargins(*PAGER_PAGE_PADDING))

        self.layoutMain = QVBoxLayout()
        self.layoutMain.setContentsMargins(
            QMargins(*NO_MARGIN)
        )
        self.layoutMain.setSpacing(PAGER_HEADER_SPACING)

        self.buttonPlayAll = TransparentTextButton(self, geometry=(0, 0, 150, 30))
        self.buttonPlayAll.setText('Play All')

        self.buttonShuffleAll = TransparentTextButton(self, geometry=(0, 0, 150, 30))
        self.buttonShuffleAll.setText('Shuffle All')

        self.layoutButtons = QHBoxLayout()
        self.layoutButtons.setContentsMargins(
            QMargins(*NO_MARGIN)
        )
        self.layoutButtons.setSpacing(PAGER_HEADER_SPACING)

        self.layoutButtons.addWidget(self.buttonPlayAll)
        self.layoutButtons.addWidget(self.buttonShuffleAll)
        self.layoutButtons.addStretch(1)

        self.listSongs = SongsList(self, geometry=PAGER_PAGE_GEO)

        self.layoutMain.addLayout(self.layoutButtons)
        self.layoutMain.addWidget(self.listSongs)
        self.setLayout(self.layoutMain)
        self.show()

    def setupEvents(self):
        self.listSongs.sig_onSongSelected.connect(self.onPlaySong)
        self.buttonPlayAll.sig_clicked.connect(self.onPlayAll)
        self.buttonShuffleAll.sig_clicked.connect(self.onShuffleAll)

    def onPlaySong(self, song):
        self.sig_onPlaySong.emit(song)

    def onPlayAll(self):
        songs = self.listSongs.listModel.getData()
        self.sig_onPlayAll.emit(songs)

    def onShuffleAll(self):
        songs = self.listSongs.listModel.getData()
        self.sig_onShuffleAll.emit(songs)


class MainFrame(QFrame):
    def __init__(self, parent=None, geometry=MAIN_PANEL_GEO):
        super(MainFrame, self).__init__(parent)
        self.initUi(geometry)

    def initUi(self, geometry):
        self.setObjectName('MainFrame')
        self.setGeometry(*geometry)
        self.setContentsMargins(
            QMargins(*MAIN_PANEL_PADDING)
        )

        # self.listSongs = SongsList(self, geometry=PAGER_PAGE_GEO)
        self.nowPlayingPage = NowPlayingPage(self, geometry=NOW_PLAYING_PAGE_GEO)
        self.songsPage = SongsPage(self, geometry=PAGER_PAGE_GEO)
        self.albumsPage = AlbumsPage(self, geometry=PAGER_PAGE_GEO)
        self.artistsPage = ArtistsPage(self, geometry=PAGER_PAGE_GEO)

        self.pager = Pager(self)
        self.pager.addPage(
            {
                'id'        : 'songs page',
                'widget'    : self.songsPage,
                'title1'    : 'Songs',
                'title2'    : 'title2',
            }
        )
        self.pager.addPage(
            {
                'id'        : 'now playing',
                'widget'    : self.nowPlayingPage,
                'title1'    : 'Now Playing',
                'title2'    : 'title2',
            }
        )
        self.pager.addPage(
            {
                'id'        : 'albums page',
                'widget'    : self.albumsPage,
                'title1'    : 'Albums',
                'title2'    : 'title2',
            }
        )
        self.pager.addPage(
            {
                'id'        : 'artists page',
                'widget'    : self.artistsPage,
                'title1'    : 'Artists',
                'title2'    : 'title2',
            }
        )

        self.pager.switchTo('songs page')

        self.layoutMain = QVBoxLayout()
        self.layoutMain.setContentsMargins(
            QMargins(*NO_MARGIN)
        )
        self.layoutMain.setSpacing(MAIN_PANEL_SPACING)

        self.layoutMain.addWidget(self.pager)

        self.setLayout(self.layoutMain)
        self.show()
