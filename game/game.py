import logging

from game import moves
from game.mazefield import load_field, coordinate

logger = logging.getLogger(__name__)


class Game(object):
    def __init__(self, player, field="default"):
        self.player = player
        logger.info("Welcome {}".format(self.player.name))
        self.field = load_field(field)
        self.current_position = self.field.get_start_position()

        logger.debug("Start position is {}".format(self.current_position))

    def play_one_turn(self):
        surroundings = self.field.get_surrounding(self.current_position)
        logger.debug("Surroundings {}".format(surroundings))
        move = self.player.turn(surroundings)
        logger.debug("Player {} moves {}".format(self.player.name, move))
        next_position = self._determine_new_coordinate(move)
        if self.field.is_move_possible(next_position):
            if self.field.is_finish(next_position):
                logger.info("{} reached finish".format(self.player.name))
                return True
            else:
                print('{} did not reach finish'.format(self.player.name))
                self.current_position = next_position
                return False

    def _determine_new_coordinate(self, move):
        if move == moves.DOWN:
           return coordinate(y=self.current_position.y + 1, x=self.current_position.x)

        if move == moves.UP:
            return coordinate(y=self.current_position.y - 1, x=self.current_position.x)

        if move == moves.LEFT:
            return coordinate(y=self.current_position.y, x=self.current_position.x - 1)

        if move == moves.RIGHT:
            return coordinate(y=self.current_position.y, x=self.current_position.x + 1)
