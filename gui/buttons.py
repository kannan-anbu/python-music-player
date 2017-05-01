from gui.widgets import *


class PlayPauseButton(TransparentImageButton):
    STATE_PLAY = 'play'
    STATE_PAUSE = 'pause'
    sig_playpause = pyqtSignal(name='sig_playpause')

    def __init__(self, parent=None, geometry=(0, 0, 10, 10)):
        super(PlayPauseButton, self).__init__(parent, geometry)

    def initUi(self, geometry):
        super().initUi(geometry)
        self.img_play = QPixmap('img/play_circle.png')
        self.img_pause = QPixmap('img/pause_circle.png')
        self.STATE = PlayPauseButton.STATE_PLAY
        self.updateUi()

    def setState(self, state):
        if self.STATE is not state:
            self.STATE = state
            self.updateUi()

    def getState(self):
        return self.STATE

    def updateUi(self):
        if self.STATE is PlayPauseButton.STATE_PLAY:
            self.setImage(self.img_play)
        else:
            self.setImage(self.img_pause)

    def mouseReleaseEvent(self, QMouseEvent):
        self.sig_playpause.emit()


class LoopButton(TransparentImageButton):
    STATE_LOOP_OFF = 'loop_off'
    STATE_LOOP_SINGLE = 'loop_single'
    STATE_LOOP_ALL = 'loop_all'
    sig_loop = pyqtSignal(name='sig_loop')

    def __init__(self, parent=None, geometry=(0, 0, 10, 10)):
        super(LoopButton, self).__init__(parent, geometry)

    def initUi(self, geometry):
        super().initUi(geometry)
        self.img_loop_off = QPixmap('img/loop_off.png')
        self.img_loop_single = QPixmap('img/loop_one.png')
        self.img_loop_all = QPixmap('img/loop_all.png')
        self.STATE = LoopButton.STATE_LOOP_OFF
        self.updateUi()

    def setState(self, state):
        if self.STATE is not state:
            self.STATE = state
            self.updateUi()

    def getState(self):
        return self.STATE

    def updateUi(self):
        if self.STATE is LoopButton.STATE_LOOP_OFF:
            self.setImage(self.img_loop_off)
        elif self.STATE is LoopButton.STATE_LOOP_SINGLE:
            self.setImage(self.img_loop_single)
        else:
            self.setImage(self.img_loop_all)

    def mouseReleaseEvent(self, QMouseEvent):
        self.sig_loop.emit()


class ShuffleButton(TransparentImageButton):
    STATE_SHUFFLE_OFF = 'shuffle_off'
    STATE_SHUFFLE_ON = 'shuffle_on'
    sig_shuffle = pyqtSignal(name='sig_shuffle')

    def __init__(self, parent=None, geometry=(0, 0, 10, 10)):
        super(ShuffleButton, self).__init__(parent, geometry)

    def initUi(self, geometry):
        super().initUi(geometry)
        self.img_shuffle_off = QPixmap('img/shuffle_off.png')
        self.img_shuffle_on = QPixmap('img/shuffle_on.png')
        self.STATE = ShuffleButton.STATE_SHUFFLE_OFF
        self.updateUi()

    def setState(self, state):
        if self.STATE is not state:
            self.STATE = state
            self.updateUi()

    def getState(self):
        return self.STATE

    def updateUi(self):
        if self.STATE is ShuffleButton.STATE_SHUFFLE_OFF:
            self.setImage(self.img_shuffle_off)
        else:
            self.setImage(self.img_shuffle_on)

    def mouseReleaseEvent(self, QMouseEvent):
        self.sig_shuffle.emit()


class NextButton(TransparentImageButton):

    sig_next = pyqtSignal(name='sig_next')

    def __init__(self, parent=None, geometry=(0, 0, 10, 10)):
        super(NextButton, self).__init__(parent, geometry)

    def initUi(self, geometry):
        super().initUi(geometry)
        self.img_next = QPixmap('img/skip_next.png')
        self.updateUi()

    def updateUi(self):
        self.setImage(self.img_next)

    def mouseReleaseEvent(self, QMouseEvent):
        self.sig_next.emit()


class PrevButton(TransparentImageButton):

    sig_prev = pyqtSignal(name='sig_prev')

    def __init__(self, parent=None, geometry=(0, 0, 10, 10)):
        super(PrevButton, self).__init__(parent, geometry)

    def initUi(self, geometry):
        super().initUi(geometry)
        self.img_prev = QPixmap('img/skip_previous.png')
        self.updateUi()

    def updateUi(self):
        self.setImage(self.img_prev)

    def mouseReleaseEvent(self, QMouseEvent):
        self.sig_prev.emit()


class NavButton(TransparentImageButton):

    sig_clicked = pyqtSignal(name='sig_clicked')

    def __init__(self, parent=None, geometry=(0, 0, 10, 10)):
        super(NavButton, self).__init__(parent, geometry)

    def initUi(self, geometry):
        super().initUi(geometry)

    def setIcon(self, iconPixmap):
        self.icon = iconPixmap
        self.updateUi()

    def updateUi(self):
        self.setImage(self.icon)

    def mouseReleaseEvent(self, QMouseEvent):
        self.sig_clicked.emit()
