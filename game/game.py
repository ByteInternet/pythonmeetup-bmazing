import logging
from .views.viewfactory import get_view
from .exceptions import MaximumTurnsReached
from .mazefield import coordinate
from .moves import *

logger = logging.getLogger(__name__)


class Game(object):
    def __init__(self, player, field, maximum_turns=300, displayname=None):
        self._field = field
        self._player = player
        self._current_position = self._field.get_start_position()
        self._current_turn = 0
        self._maximum_turns = maximum_turns
        self._maze_view = get_view(displayname)(self._field)

    def get_current_position(self):
        return self._current_position

    def get_current_turn(self):
        return self._current_turn

    def play_turn(self):
        """
        Play a turn using the players logic and the defined field
        :return: Whether the finish is reached
        :rtype: bool
        """

        self._current_turn += 1
        surroundings = self._field.get_surrounding(self._current_position)
        try:
            move = self._player.turn(surroundings)
        except Exception:
            logger.exception("The code raised an exception in turn {}".format(self.get_current_turn()))
            move = None
        new_coordinate = self._determine_new_coordinate(move)
        logger.info("Player move {} to coordinate {}".format(move, new_coordinate))
        if self._field.can_move_to_coordinate(new_coordinate):
            self._maze_view.move_player(self._current_position, new_coordinate)
            self._current_position = new_coordinate
        else:
            logger.warn("Cannot move to {}".format(move))

        finish_reached = self._field.is_finish(self._current_position)
        if not finish_reached and self._current_turn >= self._maximum_turns:
            raise MaximumTurnsReached()

        return finish_reached

    def _determine_new_coordinate(self, move):
        if move not in [DOWN, UP, LEFT, RIGHT]:
            return self._current_position

        if move == DOWN:
           return coordinate(y=self._current_position.y + 1, x=self._current_position.x)

        if move == UP:
            return coordinate(y=self._current_position.y - 1, x=self._current_position.x)

        if move == LEFT:
            return coordinate(y=self._current_position.y, x=self._current_position.x - 1)

        if move == RIGHT:
            return coordinate(y=self._current_position.y, x=self._current_position.x + 1)
