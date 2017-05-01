import gi

from utils.log import log
from utils.songattributes import *

gi.require_version('Gst', '1.0')
from gi.repository import Gst

from utils import utils

class MusicService():

    MODE_REPEAT_OFF         = 'player_mode_repeat_off'
    MODE_REPEAT_ONE         = 'player_mode_repeat_one'
    MODE_REPEAT_ALL         = 'player_mode_repeat_all'
    MODE_SHUFFLE_ON         = 'player_mode_shuffle_on'
    MODE_SHUFFLE_OFF        = 'player_mode_shuffle_off'
    VOLUME_DEFAULT          = 1.0
    VOLUME_MIN              = 0.0
    VOLUME_MAX              = 1.0

    def __init__(self):
        log('Gst init..')
        Gst.init()
        self.player = Gst.ElementFactory.make('playbin', 'player')
        fakesink = Gst.ElementFactory.make('fakesink', 'fakesink')
        self.player.set_property('video_sink', fakesink)

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect('message::error', self.on_error)
        bus.connect('message::eos', self.on_eos)
        bus.connect('message::state-changed', self.on_state_change)

        self.stateListeners = []
        self.queueListeners = []

        self.PLAYING = False
        self.LOADED = False     #can resume?
        self.state = None
        self.songqueue = []
        self.shuffleBackupQueue = []
        self.cursor = -1

        self.MODE_REPEAT = MusicService.MODE_REPEAT_OFF
        self.MODE_SHUFFLE = MusicService.MODE_SHUFFLE_OFF

    def loadandplay(self, song):
        self.stop()
        log('load and play...')
        self.player.set_property('uri', 'file://' + song[LOCATION])
        self.player.set_state(Gst.State.PLAYING)
        self.LOADED = True
        self.PLAYING = True


    def toggleplaypause(self):
        log('toggle play...')
        if self.LOADED:
            if self.PLAYING:
                self.pause()
            else:
                self.resume()
        else:
            self.next_forced()

    def pause(self):
        log('pausing...')
        self.player.set_state(Gst.State.PAUSED)
        self.PLAYING = False

    def resume(self):
        log('resuming...')
        self.player.set_state(Gst.State.PLAYING)
        self.PLAYING = True

    def next_forced(self):
        log('next forced...')
        if not self.songqueue:
            log('song q = []')
            return
        else:
            #even if cursor == -1 it will become 0
            self.cursor = (self.cursor + 1) % len(self.songqueue)
            self.loadandplay(self.songqueue[self.cursor])

    def next_auto(self):
        log('next auto...')
        if not self.songqueue:
            log('q = []')
            return
        else:
            if self.MODE_REPEAT is MusicService.MODE_REPEAT_OFF:
                if self.cursor + 1 < len(self.songqueue):
                    self.cursor += 1
                    self.loadandplay(self.songqueue[self.cursor])
                else:
                    self.songpos = -1
                    self.stop()
            elif self.MODE_REPEAT is MusicService.MODE_REPEAT_ALL:
                self.next_forced()
            else:
                self.loadandplay(self.songqueue[self.cursor])

    def prev_forced(self):
        log('prev forced...')
        if not self.songqueue:
            log('song q = []')
            return
        else:
            if self.cursor == -1:
                self.cursor = len(self.songqueue)
            self.cursor = (self.cursor - 1 + len(self.songqueue)) % len(self.songqueue)
            self.loadandplay(self.songqueue[self.cursor])

    def curpos(self):
        flag, position = self.player.query_position(Gst.Format.TIME)
        return position

    def seekto(self, sec):
        self.player.rewind()
        self.player.play(start=sec)

    def seekto_offset(self, sec_offset):
        self.player.set_pos(sec_offset)

    def stop(self):
        log('stopping...')
        self.player.set_state(Gst.State.NULL)
        self.LOADED = False
        self.PLAYING = False

    def play(self, songs):
        if type(songs) == type([]):
            self.addtoqueue(songs)
            self.goto(songs[0])
        else:
            self.addtoqueue([songs])
            self.goto(songs)

    def goto(self, song):
        log('goto...')
        if self.cursor != -1 and song == self.songqueue[self.cursor]:
            return
        for i in range( len(self.songqueue) ):
            if song == self.songqueue[i]:
                self.stop()
                self.cursor = i
                self.loadandplay(self.songqueue[self.cursor])
                break
        else:
            self.addtoqueue([song])
            self.play(song)

    def setqueue(self, queue):
        if self.MODE_SHUFFLE == MusicService.MODE_SHUFFLE_ON:
            self.shuffleBackupQueue = queue.copy()
            self.songqueue = utils.shuffleList(queue)
        else:
            self.songqueue = queue
            self.shuffleBackupQueue = []
        self.cursor = -1
        self.next_forced()
        self.notifyQueueListeners()

    def addtoqueue(self, queue):
        if self.MODE_SHUFFLE == MusicService.MODE_SHUFFLE_ON:
            self.shuffleBackupQueue.extend(queue.copy())
            self.songqueue.extend(utils.shuffleList(queue))
        else:
            self.songqueue.extend(queue)
            self.shuffleBackupQueue = []
        self.notifyQueueListeners()

    def delfromqueue(self):
        pass

    def clearqueue(self):
        self.songqueue = []
        self.shuffleBackupQueue = []
        self.cursor = -1
        self.stop()
        self.notifyQueueListeners()

    def currentSong(self):
        try:
            return self.songqueue[self.cursor]
        except:
            return None

    def repeatmode(self):
        return self.MODE_REPEAT

    def setrepeatmode(self, mode):
        self.MODE_REPEAT = mode

    def shufflemode(self):
        return self.MODE_SHUFFLE

    def setshufflemode(self, mode):
        if self.MODE_SHUFFLE != mode:
            self.MODE_SHUFFLE = mode

            if mode == MusicService.MODE_SHUFFLE_ON:
                if self.cursor != -1:
                    listToShuffle = self.songqueue[self.cursor+1 : ]
                    if listToShuffle:
                        shuffledList = utils.shuffleList(listToShuffle)
                        self.shuffleBackupQueue = self.songqueue.copy()
                        self.songqueue[self.cursor+1 :] = shuffledList
            else:
                if self.shuffleBackupQueue:
                    self.songqueue = self.shuffleBackupQueue.copy()
                    self.shuffleBackupQueue = []
            self.notifyQueueListeners()

    def volume(self):
        return self.VOLUME

    def setvolume(self, vol):
        vol = min(vol, MusicService.VOLUME_MAX)
        vol = max(vol, MusicService.VOLUME_MIN)
        self.VOLUME = vol
        self.player.set_volume(self.VOLUME)

    def addStateListener(self, listener):
        self.stateListeners.append(listener)

    def addQueueListener(self, listener):
        self.queueListeners.append(listener)

    def notifyStateListeners(self):
        for listener in self.stateListeners:
            listener()

    def notifyQueueListeners(self):
        for listener in self.queueListeners:
            listener()

    """ Gst Signal handlers -------------------------------------------"""
    def on_state_change(self, bus, message):
        old, new, pending = message.parse_state_changed()
        if message.src != self.player:
            return
        log(
            'GST-STATE_CHANGE:: ' +
            Gst.Element.state_get_name(old) +
            ' -> ' +
            Gst.Element.state_get_name(new)
        )
        self.notifyStateListeners()

    def on_eos(self, bus, message):
        log('GST-EOS')
        self.stop()
        self.next_auto()
        for listener in self.stateListeners:
            listener()

    def on_error(self, bus, message):
        err, dbg_info = message.parse_error()
        log('GST-ERROR'+ message.src.get_name() + ':' + err.message)
        if dbg_info:
            log('Debug info:' + dbg_info)

