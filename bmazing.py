import logging
import argparse
import time
from game.exceptions import MaximumTurnsReached
from game.game import Game
from game.mazefield import MazeField
from players import get_player_by_name

LOGLEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR
}


def start_game(mazename=None, playername=None, display=None, loglevel=None, *args, **kwargs):

    logging.basicConfig(
        level=LOGLEVELS.get(loglevel, LOGLEVELS['info']),
        format="%(module)s - %(message)s"
    )
    player = get_player_by_name(playername)
    field = MazeField.load_field(mazename)
    current_game = Game(player=player, field=field, displayname=display)
    try:
        while current_game.play_turn() is False:
            time.sleep(0.1)
    except MaximumTurnsReached:
        print("Maximum turns reached, there must be an easier way to get through the maze")
    else:
        current_game._maze_view.finish(player.name, current_game.get_current_turn())
        print("Awesome! You reached the finish in {} steps".format(current_game.get_current_turn()))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--maze', default="default", type=str, help="Name of the maze")
    parser.add_argument('-p', '--player', default="SamplePlayer", type=str, help="Name of the player (classname, and must be registered into players/__init__.py)")
    parser.add_argument('-d', '--display', default="terminal", type=str, choices=['pygame', 'terminal', 'none'], help="Select which display should be used to visualize the game")
    parser.add_argument('-l', '--loglevel', default="info", type=str, choices=['warning', 'error', 'info', 'debug'], help="Level of logging")
    argv = parser.parse_args()
    start_game(mazename=argv.maze, playername=argv.player, display=argv.display, loglevel=argv.loglevel)
