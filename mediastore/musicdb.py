import sqlite3

from config import config
from utils.log import log
from utils.songattributes import *


class MusicDb:

    def init(self):
        self.conn = sqlite3.connect(config.MUSICDB_NAME)
        #to access select cursor tuples with str indices instead of int
        #access like dict
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

    def createsongstable(self):
        createtablequery = 'CREATE TABLE IF NOT EXISTS ' + config.TABLE_SONGS + ' ( ' + \
                    ID + ' ' + 'VARCHAR' + ', ' + \
                    TITLE + ' ' + 'VARCHAR' + ', ' + \
                    ALBUM + ' ' + 'VARCHAR' + ', ' + \
                    ARTIST + ' ' + 'VARCHAR' + ', ' + \
                    DURATION + ' ' + 'VARCHAR' + ', ' + \
                    YEAR + ' ' + 'VARCHAR' + ', ' + \
                    GENRE + ' ' + 'VARCHAR' + ', ' + \
                    TRACK_NO + ' ' + 'VARCHAR' + ', ' + \
                    BITRATE + ' ' + 'VARCHAR' + ', ' + \
                    SAMPLE_RATE + ' ' + 'VARCHAR' + ', ' + \
                    CHANNELS + ' ' + 'VARCHAR' + ', ' + \
                    SIZE + ' ' + 'VARCHAR' + ', ' + \
                    LOCATION + ' ' + 'VARCHAR' + ', ' + \
                    USER_RATING + ' ' + 'VARCHAR' + ', ' + \
                    PLAY_COUNT + ' ' + 'VARCHAR' + \
                ');'
        log(createtablequery)
        self.cur.execute(createtablequery)
        self.conn.commit()

    def dropsongstable(self):
        dropquery = 'DROP TABLE ' + config.TABLE_SONGS + ';'
        log(dropquery)
        return self.cur.execute(dropquery)

    def clearsongstable(self):
        deletequery = 'DELETE FROM ' + config.TABLE_SONGS + ';'
        log(deletequery)
        return self.cur.execute(deletequery)

    def insertsong(self, song, commit=False):
        insertquery = 'INSERT INTO ' + config.TABLE_SONGS + ' ( '
        insertquery += ', '.join(song.keys())
        insertquery += ' ) VALUES ( '
        for _ in range(len(song)):
            insertquery += '?, '
        insertquery = insertquery[:-2]
        insertquery += ' );'
        log(insertquery)
        self.cur.execute(insertquery, tuple(song.values()))
        if commit:
            self.conn.commit()

    def deletesong(self, key, value):
        deletequery = 'DELETE FROM ' + config.TABLE_SONGS + \
            ' WHERE ' + key + ' = ?;'
        log(deletequery)
        return self.cur.execute(deletequery, (value, ))

    def getallsongs(self):
        selectquery = 'SELECT * FROM ' + config.TABLE_SONGS + \
                      ' ORDER BY (' + TITLE + ');'
        log(selectquery)
        return self.cur.execute(selectquery)

    def getAllAlbums(self):
        selectQuery = 'SELECT DISTINCT ' + ALBUM + ' FROM ' + config.TABLE_SONGS + \
                      ' ORDER BY (' + ALBUM + ');'
        log(selectQuery)
        return self.cur.execute(selectQuery)

    def getSongsForAlbum(self, album):
        selectQuery = 'SELECT * FROM ' + config.TABLE_SONGS + \
            ' WHERE ' + ALBUM + '=\'' + album + '\'' + \
                      ' ORDER BY (' + TITLE + ');'
        log(selectQuery)
        return self.cur.execute(selectQuery)

    def getAlbumSongsCount(self, album):
        selectQuery = 'SELECT COUNT(*) AS ' + SONG_COUNT + ' FROM ' + config.TABLE_SONGS + \
            ' WHERE ' + ALBUM + '=\'' + album + '\';'
        log(selectQuery)
        return self.cur.execute(selectQuery)

    def getAllArtists(self):
        selectQuery = 'SELECT DISTINCT ' + ARTIST + ' FROM ' + config.TABLE_SONGS + \
                      ' ORDER BY (' + ARTIST + ');'
        log(selectQuery)
        return self.cur.execute(selectQuery)

    def getSongsForArtist(self, artist):
        selectQuery = 'SELECT * FROM ' + config.TABLE_SONGS + \
            ' WHERE ' + ARTIST + '=\'' + artist + '\'' + \
                      ' ORDER BY (' + TITLE + ');'
        log(selectQuery)
        return self.cur.execute(selectQuery)

    def getArtistSongsCount(self, artist):
        selectQuery = 'SELECT COUNT(*) AS ' + SONG_COUNT + ' FROM ' + config.TABLE_SONGS + \
            ' WHERE ' + ARTIST + '=\'' + artist + '\';'
        log(selectQuery)
        return self.cur.execute(selectQuery)

    def getAlbumsForArtist(self, artist):
        selectQuery = 'SELECT DISTINCT ' + ALBUM + ' FROM ' + config.TABLE_SONGS + \
            ' WHERE ' + ARTIST + '=\'' + artist + '\'' + \
                      ' ORDER BY (' + ALBUM + ');'
        log(selectQuery)
        return self.cur.execute(selectQuery)

    def getsongfor_id(self, id):
        selectquery = 'SELECT * FROM ' + config.TABLE_SONGS + \
            ' WHERE ' + ID + ' = ?;'
        log(selectquery)
        return self.cur.execute(selectquery, (str(id),))

    def getsongfor_title(self, title):
        selectquery = 'SELECT * FROM ' + config.TABLE_SONGS + \
            ' WHERE ' + TITLE + ' = ?;'
        log(selectquery)
        return self.cur.execute(selectquery, (str(title),))

    def close(self):
        self.conn.commit()
        self.conn.close()
