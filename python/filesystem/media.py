import enum
import logging

from pymediainfo import MediaInfo

logger = logging.getLogger("filesystem.media")

class MediaType(enum.Enum):
    UNKNOWN = enum.auto()
    AUDIO = enum.auto()
    VIDEO = enum.auto()

def get_file_media_type(file_path):
    media_type = MediaType.UNKNOWN

    try:
        file_info = MediaInfo.parse(file_path)

        for track in file_info.tracks:
            if track.track_type == "Video":
                media_type = MediaType.VIDEO

            elif track.track_type == "Audio":
                if media_type != MediaType.VIDEO:
                    media_type = MediaType.AUDIO

    except Exception as err:
        logger.error(err, exc_info=True)

    return media_type
