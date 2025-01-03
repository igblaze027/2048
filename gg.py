import pygame
import math
import random

pygame.init()

# Constants
FPS = 60
WIN_WIDTH, WIN_HEIGHT = 1000, 600
GRID_WIDTH, GRID_HEIGHT = 600, 500
ROWS, COLS = 4, 4

RECT_HEIGHT = GRID_HEIGHT // ROWS
RECT_WIDTH = GRID_WIDTH // COLS

OUTLINE_COLOR = (187, 173, 160)
BACKGROUND_COLOR = (205, 192, 180)
FONT_COLOR = (119, 110, 101)
OUTLINE_THICKNESS = 5

# Center the grid
X_OFFSET = (WIN_WIDTH - GRID_WIDTH) // 2
Y_OFFSET = (WIN_HEIGHT - GRID_HEIGHT) // 2

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("2048")

font = pygame.font.SysFont("arial", 40, bold=True)


class Tile:
    COLORS = {
        2: (238, 228, 218),
        4: (238, 225, 201),
        8: (243, 178, 122),
        16: (246, 150, 100),
        32: (247, 124, 95),
        64: (247, 95, 59),
        128: (237, 208, 115),
        256: (237, 204, 98),
        512: (237, 201, 80),
        1024: (237, 197, 63),
        2048: (237, 194, 46)
    }

    def __init__(self, row, col, value=2):
        self.row = row
        self.col = col
        self.value = value
        self.x = X_OFFSET + col * RECT_WIDTH
        self.y = Y_OFFSET + row * RECT_HEIGHT

    def draw(self, surface):
        color = self.COLORS.get(self.value, (237, 194, 46))
        pygame.draw.rect(surface, color,
                         (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))

        text = font.render(str(self.value), True, FONT_COLOR)
        text_rect = text.get_rect(center=(self.x + RECT_WIDTH // 2,
                                          self.y + RECT_HEIGHT // 2))
        surface.blit(text, text_rect)

    def move_to(self, row, col):
        self.row = row
        self.col = col
        self.x = X_OFFSET + col * RECT_WIDTH
        self.y = Y_OFFSET + row * RECT_HEIGHT


def draw_grid():
    window.fill(BACKGROUND_COLOR)

    # Draw grid background
    pygame.draw.rect(window, OUTLINE_COLOR,
                     (X_OFFSET, Y_OFFSET, GRID_WIDTH, GRID_HEIGHT),
                     OUTLINE_THICKNESS)

    # Draw grid lines
    for i in range(1, ROWS):
        y = Y_OFFSET + i * RECT_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR,
                         (X_OFFSET, y),
                         (X_OFFSET + GRID_WIDTH, y),
                         OUTLINE_THICKNESS)

    for i in range(1, COLS):
        x = X_OFFSET + i * RECT_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR,
                         (x, Y_OFFSET),
                         (x, Y_OFFSET + GRID_HEIGHT),
                         OUTLINE_THICKNESS)


def get_empty_positions(grid):
    empty = []
    for row in range(ROWS):
        for col in range(COLS):
            if grid.get((row, col)) is None:
                empty.append((row, col))
    return empty


def add_new_tile(grid):
    empty = get_empty_positions(grid)
    if empty:
        row, col = random.choice(empty)
        value = 2 if random.random() < 0.9 else 4
        grid[(row, col)] = Tile(row, col, value)


def merge_tiles(grid, direction):
    moved = False
    merged = set()

    if direction in ['left', 'right']:
        row_range = range(ROWS)
        col_range = range(COLS - 1, -1, -1) if direction == 'right' else range(COLS)

        for row in row_range:
            for col in col_range:
                if (row, col) not in grid:
                    continue

                tile = grid[(row, col)]
                next_col = col + (1 if direction == 'right' else -1)

                while (0 <= next_col < COLS and
                       (row, next_col) not in grid):
                    next_col += (1 if direction == 'right' else -1)

                if (0 <= next_col < COLS and
                        (row, next_col) in grid and
                        grid[(row, next_col)].value == tile.value and
                        (row, next_col) not in merged):

                    grid[(row, next_col)].value *= 2
                    merged.add((row, next_col))
                    del grid[(row, col)]
                    moved = True
                else:
                    next_col = (next_col - 1 if direction == 'right'
                                else next_col + 1)
                    if next_col != col:
                        grid[(row, next_col)] = tile
                        tile.move_to(row, next_col)
                        del grid[(row, col)]
                        moved = True

    else:  # up or down
        col_range = range(COLS)
        row_range = range(ROWS - 1, -1, -1) if direction == 'down' else range(ROWS)

        for col in col_range:
            for row in row_range:
                if (row, col) not in grid:
                    continue

                tile = grid[(row, col)]
                next_row = row + (1 if direction == 'down' else -1)

                while (0 <= next_row < ROWS and
                       (next_row, col) not in grid):
                    next_row += (1 if direction == 'down' else -1)

                if (0 <= next_row < ROWS and
                        (next_row, col) in grid and
                        grid[(next_row, col)].value == tile.value and
                        (next_row, col) not in merged):

                    grid[(next_row, col)].value *= 2
                    merged.add((next_row, col))
                    del grid[(row, col)]
                    moved = True
                else:
                    next_row = (next_row - 1 if direction == 'down'
                                else next_row + 1)
                    if next_row != row:
                        grid[(next_row, col)] = tile
                        tile.move_to(next_row, col)
                        del grid[(row, col)]
                        moved = True

    return moved


def is_game_over(grid):
    if len(get_empty_positions(grid)) > 0:
        return False

    # Check for possible merges
    for row in range(ROWS):
        for col in range(COLS):
            value = grid[(row, col)].value

            # Check right
            if col < COLS - 1 and grid[(row, col + 1)].value == value:
                return False
            # Check down
            if row < ROWS - 1 and grid[(row + 1, col)].value == value:
                return False

    return True


def main():
    clock = pygame.time.Clock()
    grid = {}

    # Initialize with two tiles
    add_new_tile(grid)
    add_new_tile(grid)

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                moved = False

                if event.key == pygame.K_LEFT:
                    moved = merge_tiles(grid, 'left')
                elif event.key == pygame.K_RIGHT:
                    moved = merge_tiles(grid, 'right')
                elif event.key == pygame.K_UP:
                    moved = merge_tiles(grid, 'up')
                elif event.key == pygame.K_DOWN:
                    moved = merge_tiles(grid, 'down')

                if moved:
                    add_new_tile(grid)
                    if is_game_over(grid):
                        print("Game Over!")


        # Draw
        draw_grid()
        for tile in grid.values():
            tile.draw(window)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()