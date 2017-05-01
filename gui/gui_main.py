import sys, gi
gi.require_version('Gst', '1.0')
from mediaplayer.MusicPlayer import MusicService
from mediastore import musicstore

from gui.Frames import *
from gui.buttons import *
from utils import utils


class Gui(QWidget):

    def __init__(self, parent=None, geometry=GUI_GEO):
        super(Gui, self).__init__(parent)
        self.initUi(geometry)
        self.music_service = MusicService()
        self.setupEventCallbacks()
        self.loadLists()
        self.updateSlider()

    def initUi(self, geometry):
        self.setGeometry(*geometry)
        self.setObjectName('gui')
        self.setContentsMargins(
            QMargins(*GUI_PADDING)
        )
        self.setStyleSheet(
            """
            #gui {
                background-color: rgba(40, 40, 40, 255);
            }
            #gui QFrame#ControlsBar {
                background-color: #ff3d00
            }
            #gui QFrame#ControlsBar QWidget {
                color: white;
            }
            #gui QFrame#NavigationBar {
                background-color: rgba(21, 21, 21, 255);
            }
            #gui QFrame#MainFrame QWidget {
                background-color: rgba(40, 40, 40, 255);
                color: white;
            }
            #gui QFrame#SongDetailsFrame QLabel#Dull {
                color: rgba(225, 225, 255, 100);
            }
            """
        )

        self.navBar = NavigationBar(self)
        self.mainPanel = MainFrame(self)
        self.controlsBar = ControlsBar(self)

        layoutV = QVBoxLayout()
        layoutV.setContentsMargins(
            QMargins(*GUI_PADDING)
        )
        layoutV.setSpacing(GUI_SPACING)

        layoutH = QHBoxLayout()
        layoutH.setContentsMargins(
            QMargins(*GUI_PADDING)
        )
        layoutH.setSpacing(GUI_SPACING)

        layoutH.addWidget(self.navBar)
        layoutH.addWidget(self.mainPanel)
        layoutV.addLayout(layoutH)
        layoutV.addWidget(self.controlsBar)

        self.setLayout(layoutV)
        self.show()

    def setupEventCallbacks(self):
        self.music_service.addStateListener(self.onMusicServiceStateChanged)
        self.music_service.addQueueListener(self.onMusicServiceQueueChanged)

        self.controlsBar.buttonLoop.sig_loop.connect(self.loop)
        self.controlsBar.buttonPrev.sig_prev.connect(self.prev)
        self.controlsBar.buttonPlay.sig_playpause.connect(self.play)
        self.controlsBar.buttonNext.sig_next.connect(self.next)
        self.controlsBar.buttonShuffle.sig_shuffle.connect(self.shuffle)
        self.controlsBar.songSlider.valueChanged.connect(self.onSliderMoved)

        self.mainPanel.nowPlayingPage.songQueueFrame.listQueue.sig_onQueueSongSelected.connect(self.onQueueItemSelected)
        self.mainPanel.nowPlayingPage.songQueueFrame.clearButton.sig_clicked.connect(self.onSongQueueClear)
        self.mainPanel.songsPage.sig_onPlaySong.connect(self.onlistitemselected)
        self.mainPanel.songsPage.sig_onPlayAll.connect(lambda songs: self.music_service.play(songs))
        self.mainPanel.songsPage.sig_onShuffleAll.connect(lambda songs: self.music_service.play(utils.shuffleList(songs)))
        self.mainPanel.albumsPage.sig_onPlaySong.connect(self.onlistitemselected)
        self.mainPanel.albumsPage.sig_onPlayAlbum.connect(lambda songs: self.music_service.play(songs))
        self.mainPanel.albumsPage.sig_onShuffleAlbum.connect(lambda songs: self.music_service.play(utils.shuffleList(songs)))
        self.mainPanel.artistsPage.sig_onPlaySong.connect(self.onlistitemselected)
        self.mainPanel.artistsPage.sig_onPlayArtist.connect(lambda songs: self.music_service.play(songs))
        self.mainPanel.artistsPage.sig_onShuffleArtist.connect(lambda songs: self.music_service.play(utils.shuffleList(songs)))

        self.navBar.buttonQueue.sig_clicked.connect(lambda: self.mainPanel.pager.switchTo('now playing'))
        self.navBar.buttonSongs.sig_clicked.connect(lambda: self.gotoSongs())
        self.navBar.buttonAlbums.sig_clicked.connect(lambda: self.mainPanel.pager.switchTo('albums page'))
        self.navBar.buttonArtists.sig_clicked.connect(lambda: self.mainPanel.pager.switchTo('artists page'))

    def gotoSongs(self):
        self.mainPanel.pager.switchTo('songs page')
        self.navBar.buttonSongs.setProperty('selected', True)
        self.navBar.buttonSongs.setStyleSheet(
            self.navBar.buttonSongs.styleSheet()
        )

    def updateUi(self):
        if self.music_service.LOADED:
            song = self.music_service.currentSong()
            self.controlsBar.setTitle(song[TITLE])
            self.controlsBar.setArtist(song[ALBUM])
            self.mainPanel.nowPlayingPage.updateUi(song)
        if self.music_service.PLAYING:
            self.controlsBar.buttonPlay.setState(
                PlayPauseButton.STATE_PAUSE
            )
        else:
            self.controlsBar.buttonPlay.setState(
                PlayPauseButton.STATE_PLAY
            )

    def prev(self):
        self.music_service.prev_forced()

    def play(self):
        self.music_service.toggleplaypause()

    def next(self):
        self.music_service.next_forced()

    def loop(self):
        modeOld = self.music_service.MODE_REPEAT
        if modeOld == MusicService.MODE_REPEAT_OFF:
            modeNew = MusicService.MODE_REPEAT_ONE
            state = LoopButton.STATE_LOOP_SINGLE
        elif modeOld == MusicService.MODE_REPEAT_ONE:
            modeNew = MusicService.MODE_REPEAT_ALL
            state = LoopButton.STATE_LOOP_ALL
        else:
            modeNew = MusicService.MODE_REPEAT_OFF
            state = LoopButton.STATE_LOOP_OFF
        self.music_service.setrepeatmode(modeNew)
        self.controlsBar.buttonLoop.setState(state)

    def shuffle(self):
        if self.music_service.MODE_SHUFFLE == MusicService.MODE_SHUFFLE_ON:
            self.music_service.setshufflemode(MusicService.MODE_SHUFFLE_OFF)
            self.controlsBar.buttonShuffle.setState(ShuffleButton.STATE_SHUFFLE_OFF)
        else:
            self.music_service.setshufflemode(MusicService.MODE_SHUFFLE_ON)
            self.controlsBar.buttonShuffle.setState(ShuffleButton.STATE_SHUFFLE_ON)

    def loadLists(self):
        ms = musicstore.MusicStore()
        ms.init()

        songs = ms.getAllSongs()
        self.mainPanel.songsPage.listSongs.setdataSource(songs)

        albums = ms.getAllAlbums()
        self.mainPanel.albumsPage.listAlbums.setdataSource(albums)

        artists = ms.getAllArtists()
        self.mainPanel.artistsPage.listArtists.setdataSource(artists)

        ms.close()

    def onQueueItemSelected(self, song):
        self.music_service.goto(song)

    def onSongQueueClear(self):
        self.music_service.clearqueue()
        self.mainPanel.nowPlayingPage.songDetailsFrame.clearUi()
        self.controlsBar.clearUi()

    def onlistitemselected(self, song):
        self.music_service.play(song)

    def onMusicServiceStateChanged(self):
        self.updateUi()

    def onMusicServiceQueueChanged(self):
        self.mainPanel.nowPlayingPage.songQueueFrame.listQueue.setdataSource(
            self.music_service.songqueue
        )

    def onSliderMoved(self, event):
        pass

    def updateSlider(self):
        try:
            position = self.music_service.curpos()
            song = self.music_service.currentSong()
            if song is not None:
                duration = int(song[DURATION])
                progress = position / duration
                self.controlsBar.songSlider.setValue(int(progress * 1000))
                self.controlsBar.labelTimeElapsed.setText(formatTimeMillis(position))
                self.controlsBar.labelTimeTotal.setText(formatTimeMillis(duration))
        finally:
            QTimer.singleShot(500, self.updateSlider)


def startApp():
    app = QApplication(sys.argv)
    gui = Gui()
    sys.exit(app.exec_())


