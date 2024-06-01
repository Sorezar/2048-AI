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
clock = pygame.time.Clock()
FPS = 60

class Tile:
    def __init__(self, value, pos):
        self.value = value
        self.pos = pos
        self.target_pos = pos
        self.moving = False

    def get_color(self):
        return TILE_COLORS.get(self.value, TILE_COLORS[2048])

    def draw(self):
        x, y = self.pos
        color = self.get_color()
        rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, color, rect)
        if self.value:
            text = font.render(str(self.value), True, TILE_FONT_COLOR)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

    def update_position(self, target_pos):
        self.target_pos = target_pos
        self.moving = True

    def interpolate(self, alpha):
        if self.moving:
            start_x, start_y = self.pos
            target_x, target_y = self.target_pos
            new_x = start_x + (target_x - start_x) * alpha
            new_y = start_y + (target_y - start_y) * alpha
            self.pos = (new_x, new_y)

    def finalize_position(self):
        self.pos = self.target_pos
        self.moving = False

class Game2048:
    def __init__(self):
        self.grid = [[Tile(0, self.get_pixel_position(j, i)) for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
        self.score = 0
        self.spawn_tile()
        self.spawn_tile()

    def get_pixel_position(self, x, y):
        return (
            x * (TILE_SIZE + TILE_PADDING) + TILE_PADDING,
            y * (TILE_SIZE + TILE_PADDING) + TILE_PADDING + SCORE_HEIGHT
        )

    def spawn_tile(self):
        empty_tiles = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.grid[i][j].value == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.grid[i][j] = Tile(2 if random.random() < 0.9 else 4, self.get_pixel_position(j, i))

    def draw(self):
        screen.fill(BACKGROUND_COLOR)
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                self.grid[i][j].draw()

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
            self.update_positions()
            self.animate()

    def move_up(self):
        moved = False
        for j in range(GRID_SIZE):
            column = [self.grid[i][j] for i in range(GRID_SIZE)]
            new_column, score = self.merge(column)
            moved |= [tile.value for tile in column] != [tile.value for tile in new_column]
            for i in range(GRID_SIZE):
                self.grid[i][j] = new_column[i]
            self.score += score
        return moved

    def move_down(self):
        moved = False
        for j in range(GRID_SIZE):
            column = [self.grid[i][j] for i in range(GRID_SIZE)]
            new_column, score = self.merge(column[::-1])
            moved |= [tile.value for tile in column] != [tile.value for tile in new_column[::-1]]
            for i in range(GRID_SIZE):
                self.grid[i][j] = new_column[::-1][i]
            self.score += score
        return moved

    def move_left(self):
        moved = False
        for i in range(GRID_SIZE):
            row = [self.grid[i][j] for j in range(GRID_SIZE)]
            new_row, score = self.merge(row)
            moved |= [tile.value for tile in row] != [tile.value for tile in new_row]
            for j in range(GRID_SIZE):
                self.grid[i][j] = new_row[j]
            self.score += score
        return moved

    def move_right(self):
        moved = False
        for i in range(GRID_SIZE):
            row = [self.grid[i][j] for j in range(GRID_SIZE)]
            new_row, score = self.merge(row[::-1])
            moved |= [tile.value for tile in row] != [tile.value for tile in new_row[::-1]]
            for j in range(GRID_SIZE):
                self.grid[i][j] = new_row[::-1][j]
            self.score += score
        return moved

    def merge(self, line):
        new_line = [tile for tile in line if tile.value != 0]
        score = 0
        for i in range(len(new_line) - 1):
            if new_line[i].value == new_line[i + 1].value:
                new_line[i].value *= 2
                score += new_line[i].value
                new_line[i + 1].value = 0
        new_line = [tile for tile in new_line if tile.value != 0]
        return new_line + [Tile(0, tile.pos) for tile in line[len(new_line):]], score

    def update_positions(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                self.grid[i][j].update_position(self.get_pixel_position(j, i))

    def animate(self):
        animation_duration = 0.5  # durée de l'animation en secondes
        steps_per_second = 60  # nombre de steps par seconde
        total_steps = int(animation_duration * steps_per_second)
        for step in range(total_steps):
            alpha = step / total_steps
            for row in self.grid:
                for tile in row:
                    tile.interpolate(alpha)
            self.draw()
            pygame.display.update()
            clock.tick(FPS)

        # Finalize positions to ensure exact placement
        for row in self.grid:
            for tile in row:
                tile.finalize_position()

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
    clock.tick(FPS)

pygame.quit()
sys.exit()
