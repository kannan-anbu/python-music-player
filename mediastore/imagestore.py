import io, traceback

from PIL import Image, ImageQt

from utils.log import log
from config.config import *



def artname(songtitle):
    return IMAGE_CACHE_DIR + 'art_orig_' + songtitle


def thumbname(songtitle):
    return IMAGE_CACHE_DIR + 'art_thumb_' + songtitle



def createimage(imgbytes, songtitle):
    try:
        img = Image.open(io.BytesIO(imgbytes))
        #jpeg does not support modes like 'L' so convert
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img = cropsquare(img)
        img.save(artname(songtitle) + '.jpg', 'JPEG')
        img.thumbnail(size=(50,50))
        img.save(thumbname(songtitle) + '.jpg', 'JPEG')
    except:
        log(traceback.format_exc())


def albumart(songtitle):
    try:
        return ImageQt.ImageQt(
            cropsquare(
                Image.open(artname(songtitle) + '.jpg')
            )
        )
    except:
        log(traceback.format_exc())
        return ImageQt.ImageQt(
            cropsquare(
                Image.open('img/example3.jpg')
            )
        )


def albumart_path(songtitle):
    try:
        path = artname(songtitle) + '.jpg'
        open(path)
        return path
    except:
        log(traceback.format_exc())
        return 'img/art_default.png'


def thumbnail_path(songtitle):
    try:
        path = thumbname(songtitle) + '.jpg'
        open(path)
        return path
    except:
        log(traceback.format_exc())
        return 'img/art_default.png'

def thumbnail(songtitle):
    try:
        pass
    except:
        log(traceback.format_exc())
        #return default img

def reset():
    pass

def cropsquare(image):
    w, h = image.size
    if w == h:  #already square
        return image
    elif w > h: #landscape
        up_x = w // 2 - h // 2
        up_y = 0
        lo_x = w // 2 + h // 2
        lo_y = h
    else:
        up_x = 0
        up_y = h // 2 - w // 2
        lo_x = w
        lo_y = h // 2 + w // 2
    return image.crop(
        (up_x, up_y, lo_x, lo_y)
    )


