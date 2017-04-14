
class Player(object):
    @property
    def name(self):
        raise NotImplementedError("Specify your name")

    def turn(self, surroundings):
        raise NotImplementedError("Write the logic how to walk to the maze here")
