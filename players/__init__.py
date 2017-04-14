from .sampleplayer import SamplePlayer
from .byteplayer import BytePlayer


def get_player_by_name(name):
    import logging
    logger = logging.getLogger(__name__)
    try:
        return globals()[name]()
    except:
        logger.error("Cannot load player {}".format(name))
        raise
