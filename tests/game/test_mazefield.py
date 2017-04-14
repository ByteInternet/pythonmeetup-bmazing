from unittest import skip

import mock
from unittest import TestCase
from game.mazefield import MazeField, DEFINITION_TO_ATTRIBUTES, coordinate, surroundings
from game.mazefield_attributes import Wall, Path, Finish, Start


class TestMazeFieldLoadField(TestCase):
    def test_that_load_field_returns_a_field_object(self):
        field = MazeField.load_field('default')
        self.assertIsInstance(field, MazeField)

    def test_that_load_field_reads_file_with_field_definition(self):
        with mock.patch('game.mazefield.open', mock.mock_open(read_data="#")) as mock_open:
            MazeField.load_field('default')
            mock_open.assert_called_once_with('./fields/default')

    def test_that_load_field_raises_ioerror_when_file_does_not_exist(self):
        with self.assertRaises(IOError):
            MazeField.load_field('doesnotexist_field')

    def test_that_load_field_raises_runtimeerror_when_no_field_definition_found(self):
        with self.assertRaises(RuntimeError):
            with mock.patch('game.mazefield.open', mock.mock_open(read_data='')) as mock_open:
                MazeField.load_field('default')

    def test_that_MazeField_is_initiated_with_parsed_data_from_file(self):
        with mock.patch('game.mazefield.MazeField') as mock_mazefield, \
                mock.patch('game.mazefield.open', mock.mock_open(read_data='#')) as mock_open:

            MazeField.load_field('default')
            mock_mazefield.assert_called_once_with([[Wall]])
            
    def test_that_loading_mazefield_can_parse_supported_field_elements(self):
        field_definition = "".join(sorted(DEFINITION_TO_ATTRIBUTES.keys()))

        with mock.patch('game.mazefield.open', mock.mock_open(read_data=field_definition)):
            field = MazeField.load_field('default')
            expected_row = [DEFINITION_TO_ATTRIBUTES[c] for c in field_definition]
            self.assertEqual(field.field, [expected_row])

    def test_that_field_of_multiple_lines_can_be_parsed(self):
        field_definition = """
#######
# # #=#
#   # #
#0# # #
###   #
#######
"""
        with mock.patch('game.mazefield.open', mock.mock_open(read_data=field_definition)):
            field = MazeField.load_field('default')
            self.assertEqual(field.field, [
                [Wall, Wall, Wall, Wall, Wall, Wall, Wall],
                [Wall, Path, Wall, Path, Wall, Finish, Wall],
                [Wall, Path, Path, Path, Wall, Path, Wall],
                [Wall, Start, Wall, Path, Wall, Path, Wall],
                [Wall, Wall, Wall, Path, Path, Path, Wall],
                [Wall, Wall, Wall, Wall, Wall, Wall, Wall],
            ])

    def test_that_a_RuntimeError_is_raised_when_field_cannot_be_parsed_due_unknown_character(self):
        with mock.patch('game.mazefield.open', mock.mock_open(read_data='?')) as mock_open:
            with self.assertRaises(RuntimeError):
                MazeField.load_field('default')

    @skip("TODO")
    def test_that_non_square_maze_definitions_are_not_accepted(self):
        pass


class MazeFieldTestStartLocation(TestCase):
    def test_that_get_start_position_returns_coordinates(self):
        f = MazeField([[Start]])
        start_position = f.get_start_position()
        self.assertIsInstance(start_position, coordinate)

    def test_that_get_start_position_returns_1_and_1(self):
        f = MazeField([[Start]])
        start_position = f.get_start_position()
        self.assertEqual(start_position, coordinate(1, 1))

    def test_that_get_start_position_returns_1_and_1(self):
        f = MazeField([
            [Wall, Wall, Wall],
            [Wall, Start, Wall],
            [Wall, Wall, Wall],
        ])
        start_position = f.get_start_position()
        self.assertEqual(start_position, coordinate(2, 2))


class MazeFieldTestGetSurroundings(TestCase):
    def test_that_get_surroundings_returns_surrounding_object(self):
        f = MazeField([
            [Wall, Wall, Wall],
            [Wall, Path, Wall],
            [Wall, Wall, Wall],
        ])
        start_position = f.get_surrounding(coordinate(2, 2))  # Path (2,2)
        self.assertIsInstance(start_position, surroundings)

    def test_that_get_surroundings_returns_walls(self):
        f = MazeField([
            [Wall, Wall, Wall],
            [Wall, Path, Wall],
            [Wall, Wall, Wall],
        ])
        start_position = f.get_surrounding(coordinate(2, 2))  # Path (2,2)
        self.assertEqual(start_position, surroundings(
            right=Wall,
            left=Wall,
            up=Wall,
            down=Wall,
        ))

    def test_that_get_surroundings_returns_attributes_of_coordinate(self):
        f = MazeField([
            [Wall, Wall, Wall, Wall],
            [Wall, Path, Path, Wall],
            [Wall, Wall, Finish, Wall],
            [Wall, Wall, Wall, Wall],
        ])
        start_position = f.get_surrounding(coordinate(3, 2))  # Path (3, 3)
        self.assertEqual(start_position, surroundings(
            right=Wall,
            left=Path,
            up=Wall,
            down=Finish,
        ))

    @skip("Definitions are still bordered with a Wall, so the end of the field is never reached")
    def test_that_get_surroundings_could_not_find_left_and_returns_none(self):
        pass


class TestMazeFieldCanMoveToCoordinate(TestCase):
    def test_that_can_move_to_position_returns_False_when_coordinate_is_a_wall(self):
        f = MazeField([[Wall]])
        can_move = f.can_move_to_coordinate(coordinate(1, 1))
        self.assertFalse(can_move)

    def test_that_can_move_to_position_returns_False_when_coordinate_is_a_path(self):
        f = MazeField([[Path]])
        can_move = f.can_move_to_coordinate(coordinate(1, 1))
        self.assertTrue(can_move)

    def test_that_can_move_to_position_returns_False_when_coordinate_is_a_finish(self):
        f = MazeField([[Finish]])
        can_move = f.can_move_to_coordinate(coordinate(1, 1))
        self.assertTrue(can_move)


class TestMazeFieldIsFinish(TestCase):
    def test_that_is_finish_returns_true_when_coordinate_is_finish(self):
        f = MazeField([[Finish]])
        is_finish = f.is_finish(coordinate(1, 1))
        self.assertTrue(is_finish)

    def test_that_is_finish_returns_true_when_coordinate_is_not_finish(self):
        f = MazeField([[Wall]])
        is_finish = f.is_finish(coordinate(1, 1))
        self.assertFalse(is_finish)
