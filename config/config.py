import os

DEBUG                   = not True

MEDIA_ROOT_DIR          = os.path.expanduser("~")
IMAGE_CACHE_DIR         = 'temp/'
if not os.path.exists(IMAGE_CACHE_DIR):
    os.makedirs(IMAGE_CACHE_DIR)

MUSICDB_NAME            = 'music_database'
TABLE_SONGS             = 'table_songs'


SAMPLE_SIZE             = -16
PLAYER_BUFF_SIZE        = 4096
PLAYER_FADEOUT_MILLIS   = 500
