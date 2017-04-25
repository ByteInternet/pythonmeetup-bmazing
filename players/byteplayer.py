from game import moves
from game.mazefield_attributes import Path, Finish
from players.player import Player


class BytePlayer(Player):
    name = "Byte"
    last = None

    def __init__(self):
        self.previous_turns = []

    def turn(self, surroundings):
        #  Keep left until we find the finish (noob way)
        move = self.determine_move(surroundings)
        self.previous_turns.append(move)
        return move

    def determine_move(self, surroundings):
        if surroundings.left == Finish:
            return moves.LEFT
        if surroundings.right == Finish:
            return moves.RIGHT
        if surroundings.up == Finish:
            return moves.UP
        if surroundings.down == Finish:
            return moves.DOWN

        if surroundings.left == Path and self._last_move() != moves.RIGHT:
            return moves.LEFT

        if surroundings.up == Path and self._last_move() != moves.DOWN:
            return moves.UP

        if surroundings.right == Path and self._last_move() != moves.LEFT:
            return moves.RIGHT

        if surroundings.down == Path and self._last_move() != moves.UP:
            return moves.DOWN

        return None

    def _last_move(self):
        if len(self.previous_turns) > 0:
            return self.previous_turns[-1]
