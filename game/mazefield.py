import logging
import os
from collections import namedtuple
from .mazefield_attributes import Path, Finish, Wall, Start

logger = logging.getLogger(__name__)
FIELD_LOCATION = "./fields/"

DEFINITION_TO_ATTRIBUTES = {
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

    @staticmethod
    def load_field(field_name):
        """
        Load the MazeField using text definition
        :param field_name: name of the file containing the field definition
        :return: MazeField required for playing the game
        :rtype: MazeField
        """

        logger.debug("Loading field '{}'".format(field_name))
        definition_path = os.path.join(FIELD_LOCATION, field_name)

        if not os.path.exists(definition_path):
            logger.error("Field '{}' does not exist".format(field_name))
            raise IOError("'{}' does not exist".format(field_name))

        with open(definition_path) as fh:
            field_objects = text_to_maze_attributes(fh.readlines())
            if not field_objects:
                raise RuntimeError("No field definition found")
            return MazeField(field_objects)

    def get_start_position(self):
         for yas, xes in enumerate(self.field):
             if Start in xes:
                 return coordinate(xes.index(Start) + 1, yas + 1)

    def get_surrounding(self, coordinate):
        logger.debug("Get surroundings of coordinate {}".format(coordinate))
        left = self.field[coordinate.y - 1][coordinate.x - 1 - 1]
        right = self.field[coordinate.y - 1][coordinate.x - 1 + 1]
        up = self.field[coordinate.y - 1 - 1][coordinate.x - 1]
        down = self.field[coordinate.y - 1 + 1][coordinate.x - 1]
        return surroundings(
            left=left,
            up=up,
            right=right,
            down=down,
        )

    def can_move_to_coordinate(self, coordinate):
         object_of_coordinate = self.field[coordinate.y - 1][coordinate.x - 1]
         return object_of_coordinate is not Wall

    def is_finish(self, coordinate):
        object_of_coordinate = self.field[coordinate.y - 1][coordinate.x - 1]
        return object_of_coordinate == Finish


def text_to_maze_attributes(textfield_lines):
    """
    Convert text to arrays with field attributes
    """
    field = []
    for line in textfield_lines:
        stripped_line = line.strip('\n')
        if len(stripped_line) == 0:
            continue

        field.append([_determine_field_attribute(char) for char in stripped_line])
    return field


def _determine_field_attribute(char):
    try:
        return DEFINITION_TO_ATTRIBUTES[char]
    except KeyError:
        raise RuntimeError("Incomplete field definition, '{}' could not be translate to field attribute".format(char))
