

import copy

from game.mazefield_attributes import Wall, Finish, Start, Path

BLUE = '\033[94m'
BLUE = '\033[94m'
GREEN = '\033[92m'
GRAY = '\033[90m'
BLACK = '\033[80m'
WHITE = '\033[97m'
END = '\033[0m'

class TerminalPlayerView():
    pass


class TerminalView:
    def __init__(self, mazefield):
        self.field = mazefield

    def draw_field(self, mazefield):
        field = ""
        for row in mazefield:
            for attribute in row:
                field += self.get_draw(attribute)
                field += self.get_draw(attribute)
            field += "\n"
        return field

    def get_draw(self, attribute):
        if attribute == Wall:
            return '{}█{}'.format(GRAY, END)
        if attribute == Path:
            return '{}█{}'.format(BLACK, END)
        if attribute == Finish:
            return '{}█{}'.format(WHITE, END)
        if attribute == Start:
            return '{}█{}'.format(BLUE, END)
        if attribute == TerminalPlayerView:
            return '{}█{}'.format(GREEN, END)
        return "?"

    def add_player_position(self, new, mazefield):
        mazefield[new.y - 1][new.x - 1] = TerminalPlayerView
        return mazefield

    def move_player(self, old, new):
        mazefield = copy.deepcopy(self.field.field)
        mazefield = self.add_player_position(new, mazefield)
        print(self.draw_field(mazefield))

    def finish(self, *args, **kwargs):
        pass
