from .sampleplayer import SamplePlayer
from .byteplayer import BytePlayer


def get_player_by_name(name):
    import logging
    logger = logging.getLogger(__name__)
    try:
        return globals()[name]()
    except:
        raise RuntimeError("Cannot find player by name {}; Players are found by their classnames (case-sensitive) and should be imported into `players/__init__.py`".format(name))
