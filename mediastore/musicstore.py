import _thread, queue

from mediastore import filebrowser, metadatareader
from mediastore.musicdb import MusicDb
from utils.songattributes import *
from config.config import *


class MusicStore:

    def init(self):
        self.musicDb = MusicDb()
        self.musicDb.init()
        self.musicDb.createsongstable()

    def build(self):
        self.reBuild()

    def reBuild(self):
        self.musicDb.createsongstable()
        self.musicDb.clearsongstable()

        dq = queue.Queue()
        dq2 = queue.Queue()
        _thread.start_new_thread(filebrowser.search_files, (MEDIA_ROOT_DIR, '.mp3', dq))
        for _ in range(3):
            _thread.start_new_thread(metadatareader.getmp3metadata, (dq, dq2))
        while True:
            try:
                d = dq2.get(block=True)
                if d == 'endendend':
                    break
                self.musicDb.insertsong(d)
            except queue.Empty:
                continue

    def reset(self):
        self.musicDb.clearsongstable()

    def getAllSongs(self):
        cursor = self.musicDb.getallsongs()
        return self.cursorToList(cursor)

    def getAllAlbums(self):
        cursor = self.musicDb.getAllAlbums()
        albums = self.cursorToList(cursor)
        for album in albums:
            try:
                cur = self.musicDb.getAlbumSongsCount(album[ALBUM])
                rec = cur.fetchone()
                album[SONG_COUNT] = rec[SONG_COUNT]
            except:
                album[SONG_COUNT] = 1
        return albums

    def getSongsForAlbum(self, album):
        cursor = self.musicDb.getSongsForAlbum(album)
        return self.cursorToList(cursor)

    def getAllArtists(self):
        cursor = self.musicDb.getAllArtists()
        artists = self.cursorToList(cursor)
        for artist in artists:
            try:
                cur = self.musicDb.getArtistSongsCount(artist[ARTIST])
                rec = cur.fetchone()
                artist[SONG_COUNT] = rec[SONG_COUNT]
            except:
                artist[SONG_COUNT] = 1
        return artists

    def getSongsForArtist(self, artist):
        cursor = self.musicDb.getSongsForArtist(artist)
        return self.cursorToList(cursor)

    def getAlbumsForArtist(self, artist):
        cursor = self.musicDb.getAlbumsForArtist(artist)
        return self.cursorToList(cursor)

    def getSongForId(self, id):
        cursor = self.musicDb.getsongfor_id(id)
        return self.cursorToList(cursor)

    def getSongForTitle(self, title):
        cursor = self.musicDb.getsongfor_title(title)
        return self.cursorToList(cursor)

    def cursorToList(self, cursor):
        list = []
        for row in cursor:
            song = {}
            for key in row.keys():
                song[key] = row[key]
            list.append(song)
        return list

    def close(self):
        self.musicDb.close()
