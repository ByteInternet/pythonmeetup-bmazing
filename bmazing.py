import logging
from game.game import Game
from players.sampleplayer import SamplePlayer

logging.basicConfig(
    level=logging.DEBUG,
    format="%(module)s - %(message)s"
)

if __name__ == "__main__":
    player = SamplePlayer()
    current_game = Game(player=player)
    while current_game.play_one_turn() is False:
        pass
