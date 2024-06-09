from enum import Enum

class MsgType(Enum):
    TEXT = 'm.text'
    NOTICE = 'm.notice'
    IMAGE = 'm.image'
    VIDEO = 'm.video'
    AUDIO = 'm.audio'
    FILE = 'm.file'
    STICKER = 'm.sticker'
    LOCATION = 'm.location'

