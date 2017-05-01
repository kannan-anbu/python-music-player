from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from config.dimention import *


class ImageView(QFrame):
    def __init__(self, parent=None, geometry=(0, 0, 10, 10)):
        super(ImageView, self).__init__(parent)
        self.initUi(geometry)

    def initUi(self, geometry):
        self.setGeometry(*geometry)
        self.setContentsMargins(QMargins(0, 0, 0, 0))

        self.imageLabel = QLabel(self)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setMinimumSize(geometry[2], geometry[3])
        self.imageLabel.setMaximumSize(geometry[2], geometry[3])
        # self.imageLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.hbox = QHBoxLayout(self)
        self.hbox.setContentsMargins(QMargins(0, 0, 0, 0))
        self.hbox.addWidget(self.imageLabel)
        self.setLayout(self.hbox)
        self.show()

    def setText(self, text):
        elidedText = self.imageLabel.fontMetrics().elidedText(text, Qt.ElideRight, self.imageLabel.width())
        self.imageLabel.setText(elidedText)

    def setImage(self, pixmap):
        try:
            self.imageLabel.setPixmap(
                self.scale(pixmap)
            )
        except:
            pass

    def scale(self, pixmap):
        width = self.imageLabel.contentsRect().width()
        height = self.imageLabel.contentsRect().height()
        cs = QSize(width, height)
        s = QSize(self.geometry().width(), self.geometry().height())
        return pixmap.scaled(cs,
                             Qt.KeepAspectRatio,
                             # Qt.IgnoreAspectRatio,
                             Qt.SmoothTransformation)


class ImageButton(ImageView):

    def __init__(self, parent=None, geometry=(0, 0, 10, 10)):
        super(ImageButton, self).__init__(parent, geometry)
        self.setupEvents()

    def setupEvents(self):
        self.clicked = self.imageLabel.mousePressEvent


class TransparentImageButton(ImageButton):
    def __init__(self, parent=None, geometry=(0, 0, 10, 10)):
        super(TransparentImageButton, self).__init__(parent, geometry)
        self.setProperty('selected', False)

    def initUi(self, geometry):
        super().initUi(geometry)
        self.imageLabel.setStyleSheet(
            '''
            QLabel {
                padding: 8px;
                background-color: rgba(0, 0, 0, 0);
            }
            QLabel:hover{
                background-color: #ff3d00;
            }
            QLabel[selected=True] {
                background-color: #ff3d00;
            }
            '''
        )


class TransparentTextButton(ImageButton):

    sig_clicked = pyqtSignal(name='clicked')

    def __init__(self, parent=None, geometry=(0, 0, 10, 10)):
        super(TransparentTextButton, self).__init__(parent, geometry)

    def initUi(self, geometry):
        super().initUi(geometry)
        self.imageLabel.setStyleSheet(
            '''
            QLabel {
                padding: 5px;
                background-color: rgba(255, 255, 255, 50);
            }
            QLabel:hover{
                background-color: #ff3d00;
            }
            '''
        )

    def mouseReleaseEvent(self, QMouseEvent):
        self.sig_clicked.emit()


class Pager(QFrame):
    def __init__(self, parent=None, geometry=PAGER_GEO):
        super(Pager, self).__init__(parent)
        self.initUi(geometry)
        self.pages = []
        self.currentPageId = None

    def initUi(self, geometry):
        self.setObjectName('Pager')
        self.setGeometry(*geometry)
        self.setContentsMargins(QMargins(*PAGER_PADDING))
        self.setMinimumSize(QSize(geometry[2], geometry[3]))

        self.header = PagerHeader(self, geometry=PAGER_HEADER_GEO)

        self.layoutMain = QVBoxLayout()
        self.layoutMain.setContentsMargins(
            QMargins(*NO_MARGIN)
        )
        self.layoutMain.setSpacing(PAGER_SPACING)

        self.layoutMain.addWidget(self.header)

        self.setLayout(self.layoutMain)
        self.show()

    def addPage(self, page):
        self.pages.append(page)
        self.switchTo(self.pages[-1]['id'])

    def removePage(self):
        if len(self.pages) == 1:
            self.hidePage(self.getPage(self.pages[0]['id']))
            self.pages = []
            self.currentPageId = None
        else:
            self.hidePage(self.getPage(self.pages[-1]['id']))
            self.pages.pop()
            self.switchTo(self.pages[-1]['id'])

    def getPage(self, id):
        for page in self.pages:
            if page['id'] == id:
                return page
        return None

    def switchTo(self, id):
        if self.getPage(id) is None:
            return
        if self.currentPageId is not None \
                and id != self.currentPageId:
            oldPage = self.getPage(self.currentPageId)
            if oldPage is not None:
                self.hidePage(oldPage)

        newPage = self.getPage(id)
        self.showPage(newPage)
        self.currentPageId = id
        self.header.setTitle1(newPage['title1'])
        self.header.setTitle2(newPage['title2'])
        i = self.pages.index(newPage)
        self.pages = self.pages[:i] + self.pages[i+1:] + [newPage]

    def showPage(self, page):
        self.layoutMain.addWidget(page['widget'])
        page['widget'].show()

    def hidePage(self, page):
        self.layoutMain.removeWidget(page['widget'])
        page['widget'].hide()

    def onPageClose(self):
        self.removePage()


class PagerHeader(QFrame):
    def __init__(self, parent=None, geometry=PAGER_HEADER_GEO):
        super(PagerHeader, self).__init__(parent)
        self.initUi(geometry)

    def initUi(self, geometry):
        self.setObjectName('PagerHeader')
        self.setGeometry(*geometry)
        self.setContentsMargins(
            QMargins(*PAGER_HEADER_PADDING)
        )

        self.layoutMain = QHBoxLayout()
        self.layoutMain.setContentsMargins(
            QMargins(*NO_MARGIN)
        )
        self.layoutMain.setSpacing(PAGER_HEADER_SPACING)

        self.labelTitle1 = QLabel(self)
        f = QFont()
        f.setPixelSize(25)
        self.labelTitle1.setFont(f)
        self.labelTitle1.setText('title1')
        self.labelTitle1.setMinimumWidth(
            geometry[2] // 3
        )
        self.labelTitle1.setMaximumWidth(
            geometry[2] // 2 - 3 * PAGER_HEADER_SPACING
        )
        self.labelTitle2 = QLabel(self)
        self.labelTitle2.setText('title2')
        self.labelTitle2.setMinimumWidth(
            geometry[2] // 3
        )
        self.labelTitle2.setMaximumWidth(
            geometry[2] // 2 - 3 * PAGER_HEADER_SPACING
        )
        self.labelTitle2.hide()

        self.layoutMain.addWidget(self.labelTitle1)
        self.layoutMain.addWidget(self.labelTitle2)
        self.layoutMain.addStretch(1)

        self.setLayout(self.layoutMain)
        self.show()

    def setTitle1(self, title):
        metrics = QFontMetrics(self.labelTitle1.font())
        elidedTitle = metrics.elidedText(title, Qt.ElideRight, self.labelTitle1.width())
        self.labelTitle1.setText(elidedTitle)

    def setTitle2(self, title):
        metrics = QFontMetrics(self.labelTitle2.font())
        elidedTitle = metrics.elidedText(title, Qt.ElideRight, self.labelTitle2.width())
        self.labelTitle2.setText(elidedTitle)
