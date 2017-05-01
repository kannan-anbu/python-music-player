import os, queue

from mutagen.mp3 import MP3

from mediastore import imagestore
from utils.id3attributes import *
from utils.songattributes import *


def getmp3metadata(datainqueue, dataoutqueue):
    while True:
        while True:
            try:
                filepath = datainqueue.get(block=True)
                break
            except queue.Empty:
                continue

        if filepath == 'endendend':
            dataoutqueue.put(filepath)
            return

        metadict = {}

        try:
            mp3 = MP3(filepath)
        except:
            continue

        try:
            duration_sec = mp3.info.length
            duration_mil = duration_sec * 1000000000
            bitrate_bps = mp3.info.bitrate
            channels = mp3.info.channels
            sample_rate = mp3.info.sample_rate

            metadict[ID] = str(filepath)
            metadict[DURATION] = str(int(duration_mil))
            metadict[BITRATE] = str(bitrate_bps // 1000)
            metadict[CHANNELS] = str(channels)
            metadict[SAMPLE_RATE] = str(sample_rate)

            title = mp3.tags[ID3_TITLE].text[0] if ID3_TITLE in mp3.tags else   \
                mp3.tags[ID3_FILENAME].text[0] if ID3_FILENAME in mp3.tags else \
                filepath.split(os.sep)[-1].split('.')[0]

            album = mp3.tags[ID3_ALBUM].text[0] if ID3_ALBUM in mp3.tags else   \
                mp3.tags[ID3_ALBUM_2].text[0] if ID3_ALBUM_2 in mp3.tags else   \
                'Unknown Album'
            if album.strip() == '': album = 'Unknown Album'

            year = mp3.tags[ID3_YEAR].text[0] if ID3_YEAR in mp3.tags else  \
                mp3.tags[ID3_YEAR_2].text[0] if ID3_YEAR_2 in mp3.tags else \
                'Unknown Year'
            if year.strip() == '': year = 'Unknown Year'


            track_no = mp3.tags[ID3_TRACK_NO].text[0] if ID3_TRACK_NO in mp3.tags else '-'
            artist = mp3.tags[ID3_ARTIST].text[0] if ID3_ARTIST in mp3.tags else 'Unknown Artist'
            if artist.strip() == '': artist = 'Unknown Artist'

            metadict[TITLE] = str(title)
            metadict[ALBUM] = str(album)
            metadict[YEAR] = str(year)
            metadict[TRACK_NO] = str(track_no)
            metadict[ARTIST] = str(artist)
            metadict[LOCATION] = str(filepath)

            imgbytes = mp3.tags[ID3_ALBUM_ART].data
            if len(imgbytes) > 0:
                imagestore.createimage(imgbytes, metadict[TITLE])
        except:
            metadict[TITLE] = str(filepath.split(os.sep)[-1].split('.')[0])
            metadict[LOCATION] = str(filepath)
            metadict[ALBUM] = 'Unknown Album'
            metadict[YEAR] = 'Unknown Year'
            metadict[TRACK_NO] = '-'
            metadict[ARTIST] = 'Unknown Artist'

        dataoutqueue.put(metadict)



