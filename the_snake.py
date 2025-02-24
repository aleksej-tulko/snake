from random import choice, randint

import pygame as pg

pg.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
TURNS = {
    (pg.K_DOWN, DOWN): UP,
    (pg.K_UP, UP): DOWN,
    (pg.K_LEFT, LEFT): RIGHT,
    (pg.K_RIGHT, RIGHT): LEFT
}

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 10
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


class GameObject:
    """Parent class."""

    def __init__(self, body_color=APPLE_COLOR, occupied_cells=None) -> None:
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):
        """Will be overrided in the descendent classes."""
        raise NotImplementedError('Method Draw not defined.')

    def draw_cell(self, position):
        """Draw cell on the screen."""
        body_rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, body_rect)
        pg.draw.rect(screen, BORDER_COLOR, body_rect, 1)


class Apple(GameObject):
    """Apple attributes and methods."""

    def __init__(self, body_color=APPLE_COLOR, occupied_cells=None) -> None:
        super().__init__(body_color)
        self.position = self.randomize_position()
        self.body_color = body_color
        self.occupied_cells = occupied_cells

    def randomize_position(self):
        """Select apple position randomly on the board."""
        return (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Draw apple."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Snake attributes and methods."""

    def __init__(self, body_color=SNAKE_COLOR, length=1,
                 direction=RIGHT, last=None) -> None:
        super().__init__(body_color)
        self.positions = [self.position]
        self.body_color = body_color
        self.length = length
        self.direction = direction
        self.last = last

    def get_head_position(self):
        """Get head position."""
        return self.positions[0]

    def move(self):
        """Update position."""
        x, y = self.get_head_position()
        if self.direction == RIGHT:
            x = x + GRID_SIZE if x != SCREEN_WIDTH else 0
        elif self.direction == LEFT:
            x = x - GRID_SIZE if x != 0 else SCREEN_WIDTH
        elif self.direction == UP:
            y = y - GRID_SIZE if y != 0 else SCREEN_HEIGHT
        else:
            y = y + GRID_SIZE if y != SCREEN_HEIGHT else 0
        self.last = self.positions[-1]
        self.positions.insert(0, (x, y))
        self.occupied_cells = self.positions
        if len(self.positions) > self.length:
            self.positions.pop()

    def update_direction(self, movement):
        """Updates snake direction."""
        if movement:
            self.direction = movement

    def draw(self):
        """Draw snake."""
        self.draw_cell(self.positions[-1])
        self.draw_cell(self.get_head_position())

        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Start from the beginning."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, RIGHT, LEFT])


def handle_keys(game_object):
    """Game controller."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            for (button, arrow), direction in TURNS.items():
                if (event.key == button and direction != arrow
                        and game_object.direction != direction):
                    game_object.direction = arrow
                    return game_object.direction


def main():
    """Play"""
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        if apple.position != snake.get_head_position():
            apple.draw()
        snake.draw()
        snake.move()
        snake.update_direction(handle_keys(snake))
        if snake.get_head_position() == apple.position:
            snake.length += 1
            if apple.position in snake.occupied_cells:
                apple.position = apple.randomize_position()
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.move()
        pg.display.update()


if __name__ == '__main__':
    main()
