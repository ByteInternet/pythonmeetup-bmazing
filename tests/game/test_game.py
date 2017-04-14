from unittest import TestCase
from mock import mock
from game import moves
from game.exceptions import MaximumTurnsReached
from game.game import Game
from game.mazefield import MazeField, coordinate, surroundings
from game.mazefield_attributes import Wall, Finish, Path, Start
from players.player import Player


class FakePlayer(Player):
    def turn(self, surroundings):
        return moves.DOWN


def setup_game(player=FakePlayer(), field=None):
    if field is None:
        field = MazeField([
            [Wall, Wall, Wall],
            [Wall, Start, Wall],
            [Wall, Path, Wall],
            [Wall, Finish, Wall],
            [Wall, Wall, Wall],
        ])
    return Game(player, field)


class TestGameInitialization(TestCase):

    def test_that_game_must_be_initialized_with_player_and_field(self):
        setup_game()

    def test_that_game_sets_current_position_to_start_position_of_field_on_initialization(self):
        game = setup_game()
        current_position = game.get_current_position()
        self.assertEqual(current_position, coordinate(2, 2))

    def test_that_game_sets_current_turn_to_zero_on_initialization(self):
        game = setup_game()
        self.assertEqual(game.get_current_turn(), 0)


class TestGameMovement(TestCase):
    field = MazeField([
        [Path, Path, Path],
        [Path, Start, Path],
        [Path, Path, Path],
    ])
    player = mock.Mock()

    def setUp(self):
        self.game = setup_game(player=self.player, field=self.field)

    def test_player_can_move_left(self):
        self.player.turn.return_value = moves.LEFT

        self.game.play_turn()
        self.assertEqual(self.game.get_current_position(), coordinate(1, 2))

    def test_player_can_move_right(self):
        self.player.turn.return_value = moves.RIGHT

        self.game.play_turn()
        self.assertEqual(self.game.get_current_position(), coordinate(3, 2))

    def test_player_can_move_up(self):
        self.player.turn.return_value = moves.UP

        self.game.play_turn()
        self.assertEqual(self.game.get_current_position(), coordinate(2, 1))

    def test_player_can_move_up(self):
        self.player.turn.return_value = moves.DOWN

        self.game.play_turn()
        self.assertEqual(self.game.get_current_position(), coordinate(2, 3))


class TestGamePlayTurn(TestCase):
    def setUp(self):
        self.player = mock.Mock()
        self.player.turn.return_value = moves.DOWN

        self.game = setup_game(player=self.player)

    def test_that_play_turn_increases_current_turn(self):
        self.game.play_turn()
        self.assertEqual(self.game.get_current_turn(), 1)

    def test_that_surroundings_of_current_position_are_passed_to_players_turn(self):
        self.game.play_turn()
        self.player.turn.assert_called_once_with(surroundings(
            up=Wall,
            down=Path,
            left=Wall,
            right=Wall,
        ))

    def test_that_play_turn_changes_current_position_when_possible(self):
        self.game.play_turn()
        self.assertEqual(self.game.get_current_position(), coordinate(2, 3))

    def test_that_play_turn_keeps_current_position_when_move_is_not_possible(self):
        self.player.turn.return_value = moves.UP

        self.game.play_turn()
        self.assertEqual(self.game.get_current_position(), coordinate(2, 2))

    def test_that_play_turn_keeps_current_position_when_player_raises_exception(self):
        self.player.turn.side_effect = Exception

        self.game.play_turn()
        self.assertEqual(self.game.get_current_position(), coordinate(2, 2))

    def test_that_play_turn_returns_false_when_finish_is_not_reached(self):
        reached_finish = self.game.play_turn()
        self.assertFalse(reached_finish)

    def test_that_play_turn_returns_true_when_finish_is_reached(self):
        self.game.play_turn()
        reached_finish = self.game.play_turn()
        self.assertTrue(reached_finish)

    def test_that_maximumturnsReached_exception_is_raised_when_limit_is_reached(self):
        self.game._maximum_turns = 1

        with self.assertRaises(MaximumTurnsReached):
            self.game.play_turn()

    def test_that_maximumturnsReached_exception_is_not_raised_when_finished_is_reached_on_last_turn(self):
        self.game._maximum_turns = 2

        self.game.play_turn()
        finish = self.game.play_turn()
        self.assertTrue(finish)
