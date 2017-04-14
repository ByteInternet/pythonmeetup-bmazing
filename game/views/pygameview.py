import pygame

# Define the colors we will use in RGB format
from game.mazefield_attributes import Wall, Finish, Start

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
COORDINATE_PX_SIZE = 25


class PyGameView:
    def __init__(self, mazefield):
        self.clock = pygame.time.Clock()
        self.field = mazefield.field

        field_width = len(self.field[0]) * COORDINATE_PX_SIZE
        field_height = len(self.field) * COORDINATE_PX_SIZE
        size = [field_width, field_height]
        self.screen = pygame.display.set_mode(size)
        pygame.font.init()  # you have to call this at the start,
        # if you want to use this module.
        self.myfont = pygame.font.SysFont('Ariel', 30)

        self.draw_field_in_screen()

    def draw_field_in_screen(self):
        pygame.display.set_caption("Pythonmeetup Bmazing")

        # Clear the screen and set the screen background
        self.screen.fill(WHITE)
        line_num = 1
        for line in self.field:
            position_num = 1
            for position in line:
                if position is Wall:
                    self.draw_wall(position_num, line_num)
                if position is Finish:
                    self.draw_finish(position_num, line_num)
                if position is Start:
                    self.draw_start(position_num, line_num)
                position_num += 1

            line_num += 1

        pygame.display.flip()

    def draw_wall(self, x, y):
        self.color_box(x, y, BLACK)

    def draw_finish(self, x, y):
        self.color_box(x, y, BLUE)

    def draw_start(self, x, y):
        self.color_box(x, y, RED)
        box = [(x - 1) * COORDINATE_PX_SIZE + 5, (y - 1) * COORDINATE_PX_SIZE + 5, COORDINATE_PX_SIZE - 10, COORDINATE_PX_SIZE - 10]
        pygame.draw.rect(self.screen, BLACK, box)

    def color_box(self, x, y, color):
        box = [(x - 1) * COORDINATE_PX_SIZE, (y - 1) * COORDINATE_PX_SIZE, COORDINATE_PX_SIZE, COORDINATE_PX_SIZE]
        pygame.draw.rect(self.screen, color, box)

    def move_player(self, old, new):
        old_x, old_y = old
        new_x, new_y = new

        self.clock.tick(50)
        self.color_box(old_x, old_y, RED)
        self.color_box(new_x, new_y, RED)
        box = [(new_x - 1) * COORDINATE_PX_SIZE + 5,
               (new_y - 1) * COORDINATE_PX_SIZE + 5,
               COORDINATE_PX_SIZE - 10, COORDINATE_PX_SIZE - 10]
        pygame.draw.rect(self.screen, BLACK, box)
        pygame.display.flip()

    def finish(self, name, turns):
        textsurface = self.myfont.render('"{}" reached the finish in: {} turns.'.format(name, turns), False, (0, 255, 0))
        box = [0, 0, 1920, 50]
        for i in range(10):
            pygame.draw.rect(self.screen, (50, 50, 50), box)
            pygame.display.flip()
            self.clock.tick(2)
            self.screen.blit(textsurface, (10, 10))
            pygame.display.flip()
            self.clock.tick(1)
