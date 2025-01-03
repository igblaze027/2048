import pygame
import random

pygame.init()

SCREEN_SIZE = 700
GRID_SIZE = 4
CELL_SIZE = SCREEN_SIZE // (GRID_SIZE + 1)
PADDING = 10

COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

TEXT_COLORS = {
    2: (119, 110, 101),
    4: (119, 110, 101)
}


class Game2048:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pygame.display.set_caption('2048')
        self.font = pygame.font.SysFont('arial', 40, bold=True)
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(GRID_SIZE)
                       for j in range(GRID_SIZE) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def draw_tile(self, x, y, value):
        x_pos = x * CELL_SIZE + PADDING * (x + 1)
        y_pos = y * CELL_SIZE + PADDING * (y + 1)

        pygame.draw.rect(self.screen, COLORS.get(value, COLORS[0]),
                         (x_pos, y_pos, CELL_SIZE, CELL_SIZE),
                         border_radius=8)

        if value != 0:
            text_color = TEXT_COLORS.get(value, (255, 255, 255))
            text = self.font.render(str(value), True, text_color)
            text_rect = text.get_rect(center=(x_pos + CELL_SIZE // 2,
                                              y_pos + CELL_SIZE // 2))
            self.screen.blit(text, text_rect)

    def draw(self):
        self.screen.fill((187, 173, 160))
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                self.draw_tile(x, y, self.grid[y][x])
        pygame.display.flip()

    def move(self, direction):
        moved = False
        merged = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]

        if direction in ['LEFT', 'RIGHT']:
            for y in range(GRID_SIZE):
                row = self.grid[y]
                if direction == 'RIGHT':
                    row = row[::-1]

                # Compress
                new_row = [x for x in row if x != 0] + [0] * row.count(0)

                # Merge
                for x in range(len(new_row) - 1):
                    if new_row[x] == new_row[x + 1] != 0:
                        new_row[x] *= 2
                        self.score += new_row[x]
                        new_row[x + 1:] = new_row[x + 2:] + [0]
                        moved = True

                if direction == 'RIGHT':
                    new_row = new_row[::-1]
                if new_row != row:
                    moved = True
                self.grid[y] = new_row

        else:  # UP or DOWN
            for x in range(GRID_SIZE):
                col = [self.grid[y][x] for y in range(GRID_SIZE)]
                if direction == 'DOWN':
                    col = col[::-1]

                new_col = [x for x in col if x != 0] + [0] * col.count(0)

                for y in range(len(new_col) - 1):
                    if new_col[y] == new_col[y + 1] != 0:
                        new_col[y] *= 2
                        self.score += new_col[y]
                        new_col[y + 1:] = new_col[y + 2:] + [0]
                        moved = True

                if direction == 'DOWN':
                    new_col = new_col[::-1]
                if new_col != col:
                    moved = True
                for y in range(GRID_SIZE):
                    self.grid[y][x] = new_col[y]

        if moved:
            self.add_new_tile()
        return moved

    def game_over(self):
        if any(0 in row for row in self.grid):
            return False

        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                value = self.grid[y][x]
                if (x < GRID_SIZE - 1 and value == self.grid[y][x + 1]) or \
                        (y < GRID_SIZE - 1 and value == self.grid[y + 1][x]):
                    return False
        return True


def main():
    game = Game2048()
    running = True

    while running:
        game.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move('LEFT')
                elif event.key == pygame.K_RIGHT:
                    game.move('RIGHT')
                elif event.key == pygame.K_UP:
                    game.move('UP')
                elif event.key == pygame.K_DOWN:
                    game.move('DOWN')

                if game.game_over():
                    print(f"Game Over! Score: {game.score}")
                    running = False


if __name__ == "__main__":
    main()
    pygame.quit()