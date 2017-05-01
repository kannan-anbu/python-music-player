from pprint import pprint
from config import config


def log(message):
    if config.DEBUG:
        pprint(message)
