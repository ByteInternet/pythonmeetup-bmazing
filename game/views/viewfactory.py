from game.views.fakeview import FakeView
from game.views.terminalview import TerminalView


def get_view(name, *args, **kwargs):
    if name == 'pygame':
        from game.views.pygameview import PyGameView
        return PyGameView
    elif name == 'terminal':
        return TerminalView
    else:
        return FakeView
