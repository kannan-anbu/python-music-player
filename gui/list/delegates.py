from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from utils.songattributes import *
from utils.utils import *


class SongsListDelegate(QStyledItemDelegate):

    LIST_ITEM_PADDING = (15, 8, 15, 8)
    LIST_ITEM_ELEMENTS_SPACING = 20

    def __init__(self, parent=None):
        super(SongsListDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        painter.save()

        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        painter.setPen(QPen(Qt.NoPen))

        if option.state & QStyle.State_Selected:
            painter.setBrush(QBrush(QColor.fromRgb(255, 61, 00, 255)))
            painter.drawRect(option.rect)
        else:
            if index.row() % 2 == 0:
                painter.setBrush(QBrush(QColor.fromRgb(225, 255, 255, 20)))
            else:
                painter.setBrush(QBrush(QColor.fromRgb(225, 255, 255, 0)))
            painter.drawRect(option.rect)

            if option.state & QStyle.State_MouseOver:
                painter.setBrush(QBrush(QColor.fromRgb(255, 61, 00, 255)))
                painter.drawRect(
                    QRect(
                        option.rect.left(),
                        option.rect.top(),
                        SongsListDelegate.LIST_ITEM_PADDING[0] // 3,
                        option.rect.height(),
                    )
                )

        paddedRect = option.rect.marginsRemoved(
            QMargins(*SongsListDelegate.LIST_ITEM_PADDING)
        )

        """ image """
        imgRect = QRect (
            0,
            0,
            paddedRect.height(),
            paddedRect.height()
        )
        imgRect.moveBottomLeft(paddedRect.bottomLeft())

        """ duration """
        durationTextWidth = painter.fontMetrics().size(Qt.TextSingleLine, '00:00:00').width()
        durationRect = QRect (
            0,
            0,
            durationTextWidth,
            paddedRect.height()
        )
        durationRect.moveBottomRight(paddedRect.bottomRight())

        """ title """
        remainingWidth = paddedRect.width() - imgRect.width() - durationRect.width() - 3*SongsListDelegate.LIST_ITEM_ELEMENTS_SPACING

        titleRect = QRect (
            0,
            0,
            remainingWidth // 2,
            paddedRect.height()
        )
        titleRect.moveTopLeft(
            QPoint(
                imgRect.right() + SongsListDelegate.LIST_ITEM_ELEMENTS_SPACING,
                paddedRect.top()
            )
        )

        """ album """
        albumRect = QRect (
            0,
            0,
            remainingWidth // 2,
            paddedRect.height()
        )
        albumRect.moveTopLeft(
            QPoint(
                titleRect.right() + SongsListDelegate.LIST_ITEM_ELEMENTS_SPACING,
                paddedRect.top()
            )
        )

        """ painting """
        img = index.data(Qt.DecorationRole)
        painter.drawPixmap(imgRect, img)

        painter.setPen(QPen(Qt.white))
        song = index.data(Qt.DisplayRole)
        title = song[TITLE]
        elidedTitle = painter.fontMetrics().elidedText(title, Qt.ElideRight, titleRect.width())
        painter.drawText(titleRect, Qt.AlignLeft | Qt.AlignVCenter, elidedTitle)

        album = song[ALBUM]
        elidedAlbum = painter.fontMetrics().elidedText(album, Qt.ElideRight, albumRect.width())
        painter.drawText(albumRect, Qt.AlignLeft | Qt.AlignVCenter, elidedAlbum)

        duration = song[DURATION]
        durationText = formatTimeMillis(duration)
        painter.drawText(durationRect, Qt.AlignRight | Qt.AlignVCenter, durationText)

        painter.restore()

    def sizeHint(self, option, index):
        return QSize(15, 45)


class QueueListDelegate(QStyledItemDelegate):

    LIST_ITEM_PADDING = (15, 4, 15, 4)
    LIST_ITEM_ELEMENTS_SPACING = 20

    def __init__(self, parent=None):
        super(QueueListDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        painter.save()

        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        painter.setPen(QPen(Qt.NoPen))

        if option.state & QStyle.State_Selected:
            painter.setBrush(QBrush(QColor.fromRgb(255, 61, 00, 255)))
            painter.drawRect(option.rect)
        else:
            if index.row() % 2 == 0:
                painter.setBrush(QBrush(QColor.fromRgb(225, 255, 255, 20)))
            else:
                painter.setBrush(QBrush(QColor.fromRgb(225, 255, 255, 0)))
            painter.drawRect(option.rect)

            if option.state & QStyle.State_MouseOver:
                painter.setBrush(QBrush(QColor.fromRgb(255, 61, 00, 255)))
                painter.drawRect(
                    QRect(
                        option.rect.left(),
                        option.rect.top(),
                        SongsListDelegate.LIST_ITEM_PADDING[0] // 3,
                        option.rect.height(),
                    )
                )

        paddedRect = option.rect.marginsRemoved(
            QMargins(*SongsListDelegate.LIST_ITEM_PADDING)
        )

        numMax = index.model().rowCount() + 1

        numMaxWidth = painter.fontMetrics().size(Qt.TextSingleLine, str(numMax)).width()
        numRect = QRect (
            0,
            0,
            numMaxWidth,
            paddedRect.height()
        )
        numRect.moveBottomLeft(paddedRect.bottomLeft())

        """ duration """
        durationTextWidth = painter.fontMetrics().size(Qt.TextSingleLine, '00:00:00').width()
        durationRect = QRect (
            0,
            0,
            durationTextWidth,
            paddedRect.height()
        )
        durationRect.moveBottomRight(paddedRect.bottomRight())

        """ title """
        remainingWidth = paddedRect.width() - numRect.width() - durationRect.width() - SongsListDelegate.LIST_ITEM_ELEMENTS_SPACING

        textRect = QRect(
            0,
            0,
            remainingWidth,
            paddedRect.height()
        )
        textRect.moveTopLeft(
            QPoint(
                numRect.right() + SongsListDelegate.LIST_ITEM_ELEMENTS_SPACING,
                paddedRect.top()
            )
        )

        painter.setPen(QPen(QColor.fromRgb(255, 255, 255, 150)))
        num = index.row() + 1
        painter.drawText(numRect, Qt.AlignRight | Qt.AlignVCenter, str(num))

        painter.setPen(QPen(Qt.white))
        song = index.data(Qt.DisplayRole)

        title = song[TITLE]
        elidedTitle = painter.fontMetrics().elidedText(title, Qt.ElideRight, textRect.width())
        painter.drawText(textRect, Qt.AlignLeft | Qt.AlignVCenter, elidedTitle)

        duration = song[DURATION]
        durationText = formatTimeMillis(duration)
        painter.drawText(durationRect, Qt.AlignRight | Qt.AlignVCenter, durationText)

        painter.restore()

    def sizeHint(self, option, index):
        return QSize(15, 30)


class AlbumsListDelegate(QStyledItemDelegate):

    LIST_ITEM_PADDING = (15, 4, 15, 4)
    LIST_ITEM_ELEMENTS_SPACING = 20

    def __init__(self, parent=None):
        super(AlbumsListDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        painter.save()

        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        painter.setPen(QPen(Qt.NoPen))

        if option.state & QStyle.State_Selected:
            painter.setBrush(QBrush(QColor.fromRgb(255, 61, 00, 255)))
            painter.drawRect(option.rect)
        else:
            if index.row() % 2 == 0:
                painter.setBrush(QBrush(QColor.fromRgb(225, 255, 255, 20)))
            else:
                painter.setBrush(QBrush(QColor.fromRgb(225, 255, 255, 0)))
            painter.drawRect(option.rect)

            if option.state & QStyle.State_MouseOver:
                painter.setBrush(QBrush(QColor.fromRgb(255, 61, 00, 255)))
                painter.drawRect(
                    QRect(
                        option.rect.left(),
                        option.rect.top(),
                        SongsListDelegate.LIST_ITEM_PADDING[0] // 3,
                        option.rect.height(),
                    )
                )

        paddedRect = option.rect.marginsRemoved(
            QMargins(*SongsListDelegate.LIST_ITEM_PADDING)
        )

        """ image """
        imgRect = QRect (
            0,
            0,
            paddedRect.height(),
            paddedRect.height()
        )
        imgRect.moveBottomLeft(paddedRect.bottomLeft())

        songCountTextWidth = painter.fontMetrics().size(Qt.TextSingleLine, '99999 Songs').width()
        songCountRect = QRect (
            0,
            0,
            songCountTextWidth,
            paddedRect.height()
        )
        songCountRect.moveBottomRight(paddedRect.bottomRight())

        """ title """
        remainingWidth = paddedRect.width() - imgRect.width() - songCountRect.width() - 2*SongsListDelegate.LIST_ITEM_ELEMENTS_SPACING

        textRect = QRect(
            0,
            0,
            remainingWidth,
            paddedRect.height()
        )
        textRect.moveTopLeft(
            QPoint(
                imgRect.right() + SongsListDelegate.LIST_ITEM_ELEMENTS_SPACING,
                paddedRect.top()
            )
        )

        img = QPixmap('img/album.png')
        painter.drawPixmap(imgRect, img)

        painter.setPen(QPen(Qt.white))
        album = index.data(Qt.DisplayRole)

        title = album[ALBUM]
        elidedTitle = painter.fontMetrics().elidedText(title, Qt.ElideRight, textRect.width())
        painter.drawText(textRect, Qt.AlignLeft | Qt.AlignVCenter, elidedTitle)

        songCount = album[SONG_COUNT]
        songCountText = str(songCount) + ('  Songs' if songCount > 1 else '  Song ')
        painter.drawText(songCountRect, Qt.AlignRight | Qt.AlignVCenter, songCountText)

        painter.restore()

    def sizeHint(self, option, index):
        return QSize(15, 40)


class ArtistsListDelegate(QStyledItemDelegate):

    LIST_ITEM_PADDING = (15, 4, 15, 4)
    LIST_ITEM_ELEMENTS_SPACING = 20

    def __init__(self, parent=None):
        super(ArtistsListDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        painter.save()

        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        painter.setPen(QPen(Qt.NoPen))

        if option.state & QStyle.State_Selected:
            painter.setBrush(QBrush(QColor.fromRgb(255, 61, 00, 255)))
            painter.drawRect(option.rect)
        else:
            if index.row() % 2 == 0:
                painter.setBrush(QBrush(QColor.fromRgb(225, 255, 255, 20)))
            else:
                painter.setBrush(QBrush(QColor.fromRgb(225, 255, 255, 0)))
            painter.drawRect(option.rect)

            if option.state & QStyle.State_MouseOver:
                painter.setBrush(QBrush(QColor.fromRgb(255, 61, 00, 255)))
                painter.drawRect(
                    QRect(
                        option.rect.left(),
                        option.rect.top(),
                        SongsListDelegate.LIST_ITEM_PADDING[0] // 3,
                        option.rect.height(),
                    )
                )

        paddedRect = option.rect.marginsRemoved(
            QMargins(*SongsListDelegate.LIST_ITEM_PADDING)
        )

        """ image """
        imgRect = QRect (
            0,
            0,
            paddedRect.height(),
            paddedRect.height()
        )
        imgRect.moveBottomLeft(paddedRect.bottomLeft())

        songCountTextWidth = painter.fontMetrics().size(Qt.TextSingleLine, '99999 Songs').width()
        songCountRect = QRect (
            0,
            0,
            songCountTextWidth,
            paddedRect.height()
        )
        songCountRect.moveBottomRight(paddedRect.bottomRight())

        """ title """
        remainingWidth = paddedRect.width() - imgRect.width() - songCountRect.width() - 2*SongsListDelegate.LIST_ITEM_ELEMENTS_SPACING

        textRect = QRect(
            0,
            0,
            remainingWidth,
            paddedRect.height()
        )
        textRect.moveTopLeft(
            QPoint(
                imgRect.right() + SongsListDelegate.LIST_ITEM_ELEMENTS_SPACING,
                paddedRect.top()
            )
        )

        img = QPixmap('img/artist.png')
        painter.drawPixmap(imgRect, img)

        painter.setPen(QPen(Qt.white))
        artist = index.data(Qt.DisplayRole)

        title = artist[ARTIST]
        elidedTitle = painter.fontMetrics().elidedText(title, Qt.ElideRight, textRect.width())
        painter.drawText(textRect, Qt.AlignLeft | Qt.AlignVCenter, elidedTitle)

        songCount = artist[SONG_COUNT]
        songCountText = str(songCount) + ('  Songs' if songCount > 1 else '  Song ')
        painter.drawText(songCountRect, Qt.AlignRight | Qt.AlignVCenter, songCountText)

        painter.restore()

    def sizeHint(self, option, index):
        return QSize(15, 40)


class AlbumSongsListDelegate(QStyledItemDelegate):

    LIST_ITEM_PADDING = (15, 8, 15, 8)
    LIST_ITEM_ELEMENTS_SPACING = 20

    def __init__(self, parent=None):
        super(AlbumSongsListDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        painter.save()

        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        painter.setPen(QPen(Qt.NoPen))
        if option.state & QStyle.State_Selected:
            painter.setBrush(QBrush(QColor.fromRgb(255, 61, 00, 255)))
            painter.drawRect(option.rect)
        else:
            if index.row() % 2 == 0:
                painter.setBrush(QBrush(QColor.fromRgb(225, 255, 255, 20)))
            else:
                painter.setBrush(QBrush(QColor.fromRgb(225, 255, 255, 0)))
            painter.drawRect(option.rect)

            if option.state & QStyle.State_MouseOver:
                painter.setBrush(QBrush(QColor.fromRgb(255, 61, 00, 255)))
                painter.drawRect(
                    QRect(
                        option.rect.left(),
                        option.rect.top(),
                        SongsListDelegate.LIST_ITEM_PADDING[0] // 3,
                        option.rect.height(),
                    )
                )

        paddedRect = option.rect.marginsRemoved(
            QMargins(*SongsListDelegate.LIST_ITEM_PADDING)
        )

        """ image """
        imgRect = QRect (
            0,
            0,
            paddedRect.height(),
            paddedRect.height()
        )
        imgRect.moveBottomLeft(paddedRect.bottomLeft())

        """ duration """
        font = QFont()
        fontMetrics = QFontMetrics(font)
        durationTextWidth = fontMetrics.size(Qt.TextSingleLine, '00:00:00')
        durationRect = QRect (
            0,
            0,
            durationTextWidth.width(),
            paddedRect.height()
        )
        durationRect.moveBottomRight(paddedRect.bottomRight())

        """ title """
        remainingWidth = paddedRect.width() - imgRect.width() - durationRect.width() - 3*SongsListDelegate.LIST_ITEM_ELEMENTS_SPACING

        titleRect = QRect (
            0,
            0,
            remainingWidth // 2,
            paddedRect.height()
        )
        titleRect.moveTopLeft(
            QPoint(
                imgRect.right() + SongsListDelegate.LIST_ITEM_ELEMENTS_SPACING,
                paddedRect.top()
            )
        )

        """ artist """
        artistRect = QRect (
            0,
            0,
            remainingWidth // 2,
            paddedRect.height()
        )
        artistRect.moveTopLeft(
            QPoint(
                titleRect.right() + SongsListDelegate.LIST_ITEM_ELEMENTS_SPACING,
                paddedRect.top()
            )
        )

        """ painting """
        img = index.data(Qt.DecorationRole)
        painter.drawPixmap(imgRect, img)

        painter.setPen(QPen(Qt.white))
        song = index.data(Qt.DisplayRole)
        title = song[TITLE]
        elidedTitle = painter.fontMetrics().elidedText(title, Qt.ElideRight, titleRect.width())
        painter.drawText(titleRect, Qt.AlignLeft | Qt.AlignVCenter, elidedTitle)

        album = song[ARTIST]
        elidedAlbum = painter.fontMetrics().elidedText(album, Qt.ElideRight, artistRect.width())
        painter.drawText(artistRect, Qt.AlignLeft | Qt.AlignVCenter, elidedAlbum)

        duration = song[DURATION]
        durationText = formatTimeMillis(duration)
        painter.drawText(durationRect, Qt.AlignRight | Qt.AlignVCenter, durationText)

        painter.restore()

    def sizeHint(self, option, index):
        return QSize(15, 45)


class ArtistSongsListDelegate(QStyledItemDelegate):

    LIST_ITEM_PADDING = (15, 8, 15, 8)
    LIST_ITEM_ELEMENTS_SPACING = 20

    def __init__(self, parent=None):
        super(ArtistSongsListDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        painter.save()

        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        painter.setPen(QPen(Qt.NoPen))
        if option.state & QStyle.State_Selected:
            painter.setBrush(QBrush(QColor.fromRgb(255, 61, 00, 255)))
            painter.drawRect(option.rect)
        else:
            if index.row() % 2 == 0:
                painter.setBrush(QBrush(QColor.fromRgb(225, 255, 255, 20)))
            else:
                painter.setBrush(QBrush(QColor.fromRgb(225, 255, 255, 0)))
            painter.drawRect(option.rect)

            if option.state & QStyle.State_MouseOver:
                painter.setBrush(QBrush(QColor.fromRgb(255, 61, 00, 255)))
                painter.drawRect(
                    QRect(
                        option.rect.left(),
                        option.rect.top(),
                        SongsListDelegate.LIST_ITEM_PADDING[0] // 3,
                        option.rect.height(),
                    )
                )

        paddedRect = option.rect.marginsRemoved(
            QMargins(*SongsListDelegate.LIST_ITEM_PADDING)
        )

        """ image """
        imgRect = QRect (
            0,
            0,
            paddedRect.height(),
            paddedRect.height()
        )
        imgRect.moveBottomLeft(paddedRect.bottomLeft())

        """ duration """
        font = QFont()
        fontMetrics = QFontMetrics(font)
        durationTextWidth = fontMetrics.size(Qt.TextSingleLine, '00:00:00')
        durationRect = QRect (
            0,
            0,
            durationTextWidth.width(),
            paddedRect.height()
        )
        durationRect.moveBottomRight(paddedRect.bottomRight())

        """ title """
        remainingWidth = paddedRect.width() - imgRect.width() - durationRect.width() - 3*SongsListDelegate.LIST_ITEM_ELEMENTS_SPACING

        titleRect = QRect (
            0,
            0,
            remainingWidth // 2,
            paddedRect.height()
        )
        titleRect.moveTopLeft(
            QPoint(
                imgRect.right() + SongsListDelegate.LIST_ITEM_ELEMENTS_SPACING,
                paddedRect.top()
            )
        )

        """ album """
        albumRect = QRect (
            0,
            0,
            remainingWidth // 2,
            paddedRect.height()
        )
        albumRect.moveTopLeft(
            QPoint(
                titleRect.right() + SongsListDelegate.LIST_ITEM_ELEMENTS_SPACING,
                paddedRect.top()
            )
        )

        """ painting """
        img = index.data(Qt.DecorationRole)
        painter.drawPixmap(imgRect, img)

        painter.setPen(QPen(Qt.white))
        song = index.data(Qt.DisplayRole)
        title = song[TITLE]
        elidedTitle = painter.fontMetrics().elidedText(title, Qt.ElideRight, titleRect.width())
        painter.drawText(titleRect, Qt.AlignLeft | Qt.AlignVCenter, elidedTitle)

        album = song[ALBUM]
        elidedAlbum = painter.fontMetrics().elidedText(album, Qt.ElideRight, albumRect.width())
        painter.drawText(albumRect, Qt.AlignLeft | Qt.AlignVCenter, elidedAlbum)

        duration = song[DURATION]
        durationText = formatTimeMillis(duration)
        painter.drawText(durationRect, Qt.AlignRight | Qt.AlignVCenter, durationText)

        painter.restore()

    def sizeHint(self, option, index):
        return QSize(15, 45)
