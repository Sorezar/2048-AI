import pygame
import sys
import random

# Couleurs
BACKGROUND_COLOR = (189, 173, 159)
EMPTY_COLOR = (207, 193, 180, 255)
TILE_COLORS = {
    2: (239, 233, 226),
    4: (239, 230, 212),
    8: (237, 192, 148),
    16: (254, 155, 96),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (242, 192, 57),
    2048: (237, 194, 46),
}
TILE_FONT_COLOR = (119, 110, 101)
SCORE_COLOR = (119, 110, 101)

# Dimensions
GRID_SIZE = 4
TILE_SIZE = 100
TILE_PADDING = 15
SCREEN_SIZE = GRID_SIZE * TILE_SIZE + (GRID_SIZE + 1) * TILE_PADDING
SCORE_HEIGHT = 50

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE + SCORE_HEIGHT))
pygame.display.set_caption("2048")
font = pygame.font.SysFont("arial", 40)
score_font = pygame.font.SysFont("arial", 30)

class Game2048:
    def __init__(self):
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.spawn_tile()
        self.spawn_tile()

    def spawn_tile(self):
        empty_tiles = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.grid[i][j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def draw(self):
        screen.fill(BACKGROUND_COLOR)
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = self.grid[i][j]
                color = TILE_COLORS.get(value, TILE_COLORS[2048])
                rect = pygame.Rect(j * (TILE_SIZE + TILE_PADDING) + TILE_PADDING,
                                   i * (TILE_SIZE + TILE_PADDING) + TILE_PADDING + SCORE_HEIGHT,
                                   TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, color, rect)
                if value:
                    text = font.render(str(value), True, TILE_FONT_COLOR)
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)

        score_text = score_font.render(f"Score: {self.score}", True, SCORE_COLOR)
        screen.blit(score_text, (10, 10))

    def move(self, direction):
        moved = False
        if direction == "UP":
            moved = self.move_up()
        elif direction == "DOWN":
            moved = self.move_down()
        elif direction == "LEFT":
            moved = self.move_left()
        elif direction == "RIGHT":
            moved = self.move_right()
        if moved:
            self.spawn_tile()

    def move_up(self):
        moved = False
        for j in range(GRID_SIZE):
            column = [self.grid[i][j] for i in range(GRID_SIZE)]
            new_column, score = self.merge(column)
            moved |= column != new_column
            for i in range(GRID_SIZE):
                self.grid[i][j] = new_column[i]
            self.score += score
        return moved

    def move_down(self):
        moved = False
        for j in range(GRID_SIZE):
            column = [self.grid[i][j] for i in range(GRID_SIZE)]
            new_column, score = self.merge(column[::-1])
            moved |= column != new_column[::-1]
            for i in range(GRID_SIZE):
                self.grid[i][j] = new_column[::-1][i]
            self.score += score
        return moved

    def move_left(self):
        moved = False
        for i in range(GRID_SIZE):
            row = self.grid[i]
            new_row, score = self.merge(row)
            moved |= row != new_row
            self.grid[i] = new_row
            self.score += score
        return moved

    def move_right(self):
        moved = False
        for i in range(GRID_SIZE):
            row = self.grid[i]
            new_row, score = self.merge(row[::-1])
            moved |= row != new_row[::-1]
            self.grid[i] = new_row[::-1]
            self.score += score
        return moved

    def merge(self, line):
        new_line = [i for i in line if i != 0]
        score = 0
        for i in range(len(new_line) - 1):
            if new_line[i] == new_line[i + 1]:
                new_line[i] *= 2
                score += new_line[i]
                new_line[i + 1] = 0
        new_line = [i for i in new_line if i != 0]
        return new_line + [0] * (GRID_SIZE - len(new_line)), score

game = Game2048()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.move("UP")
            elif event.key == pygame.K_DOWN:
                game.move("DOWN")
            elif event.key == pygame.K_LEFT:
                game.move("LEFT")
            elif event.key == pygame.K_RIGHT:
                game.move("RIGHT")

    game.draw()
    pygame.display.update()

pygame.quit()
sys.exit()
