from unittest import TestCase

import mock

from game.mazefield import MazeField
from game.mazefield_attributes import Wall, Start, Path, Finish
from game.views.pygameview import PyGameView


class TestPygameView(TestCase):
    def setUp(self):
        self.mazefield = MazeField([
            [Wall, Wall, Wall],
            [Wall, Start, Wall],
            [Wall, Path, Wall],
            [Wall, Path, Wall],
            [Wall, Finish, Wall],
            [Wall, Wall, Wall],
        ])

    def test_that_pygame_view_gets_size_from_fields(self):
        with mock.patch('game.views.pygameview.pygame') as mock_pygame:
            PyGameView(self.mazefield)
            mock_pygame.display.set_mode.assert_called_once_with([75, 150])

    def test_that_pygame_view_screen_is_white(self):
        screen = mock.Mock()
        with mock.patch('game.views.pygameview.pygame') as mock_pygame:
            mock_pygame.display.set_mode.return_value = screen
            PyGameView(self.mazefield)
            screen.fill.assert_called_once_with((255, 255, 255))

    def test_that_pygame_draws_black_for_walls(self):
        with mock.patch('game.views.pygameview.pygame'):
            mazeview = PyGameView(self.mazefield)
            with mock.patch('game.views.pygameview.PyGameView.color_box') as mock_color_box:
                mazeview.draw_wall(1, 1)
                mock_color_box.assert_called_once_with(1, 1, (0, 0, 0))

    def test_that_pygame_draws_blue_for_finish(self):
        with mock.patch('game.views.pygameview.pygame'):
            mazeview = PyGameView(self.mazefield)
            with mock.patch('game.views.pygameview.PyGameView.color_box') as mock_color_box:
                mazeview.draw_finish(1, 1)
                mock_color_box.assert_called_once_with(1, 1, (0, 0, 255))

    def test_that_pygame_draws_red_for_start(self):
        with mock.patch('game.views.pygameview.pygame'):
            mazeview = PyGameView(self.mazefield)
            with mock.patch('game.views.pygameview.PyGameView.color_box') as mock_color_box:
                mazeview.draw_start(1, 1)
                mock_color_box.assert_called_once_with(1, 1, (255, 0, 0))

    def test_that_pygame_draws_14_walls(self):
        with mock.patch('game.views.pygameview.pygame') as mock_pygame:
            with mock.patch('game.views.pygameview.PyGameView.draw_wall') as mock_draw_wall:
                PyGameView(self.mazefield)
                self.assertEqual(mock_draw_wall.call_count, 14)

    def test_that_pygame_draws_1_finish(self):
        with mock.patch('game.views.pygameview.pygame') as mock_pygame:
            with mock.patch('game.views.pygameview.PyGameView.draw_finish') as mock_draw_finish:
                PyGameView(self.mazefield)
                mock_draw_finish.assert_called_once_with(2, 5)

    def test_that_pygame_draws_1_start(self):
        with mock.patch('game.views.pygameview.pygame') as mock_pygame:
            with mock.patch('game.views.pygameview.PyGameView.draw_start') as mock_draw_start:
                PyGameView(self.mazefield)
                mock_draw_start.assert_called_once_with(2, 2)
