import logging
import os
from collections import namedtuple
from game.mazefield_attributes import Path, Finish, Wall, Start

logger = logging.getLogger(__name__)
FIELD_LOCATION = "./fields/"

DEFINITION_TO_OBJECT = {
    '0': Start,
    ' ': Path,
    '#': Wall,
    '=': Finish
}

coordinate = namedtuple('Coordinate', ['x', 'y'])
surroundings = namedtuple('Surroundings', ['left', 'up', 'right', 'down'])


class MazeField(object):
    def __init__(self, field):
        self.field = field
        logger.debug("Loaded field of dimension {}x{}".format(len(self.field), len(self.field[0])))

    def get_start_position(self):
        for yas, xes in enumerate(self.field):
            if Start in xes:
                return coordinate(xes.index(Start) + 1, yas + 1)

    def get_surrounding(self, coordinate):
        logger.debug("Get surroundings of coordinate {}".format(coordinate))
        left = self.field[coordinate.y - 1][coordinate.x - 1 - 1]
        right = self.field[coordinate.y - 1][coordinate.x - 1 + 1]
        up = self.field[coordinate.y - 1 - 1][coordinate.x]
        down = self.field[coordinate.y - 1 + 1][coordinate.x]
        return surroundings(
            left=left,
            up=up,
            right=right,
            down=down,
        )

    def is_move_possible(self, coordinate):
        object_of_coordinate = self.field[coordinate.y - 1][coordinate.x - 1]
        return object_of_coordinate is not Wall

    def is_finish(self, coordinate):
        object_of_coordinate = self.field[coordinate.y - 1][coordinate.x - 1]
        return object_of_coordinate == Finish



def load_field(field_name):
    logger.debug("Loading field '{}'".format(field_name))
    definition_path = os.path.join(FIELD_LOCATION, field_name)
    if not os.path.exists(definition_path):
        logger.error("Field '{}' does not exist".format(field_name))
        raise IOError("'{}' does not exist".format(field_name))

    with open(definition_path) as fh:
        return MazeField(parse_field(fh.readlines()))


def parse_field(textfield_lines):
    field = []
    for line in textfield_lines:
        field.append([_determine_field_object(char) for char in line.strip()])
    return field


def _determine_field_object(char):
    try:
        return DEFINITION_TO_OBJECT[char]
    except KeyError:
        raise RuntimeError("Incomplete field definition, '{}' could not be translate to field attribute".format(char))

