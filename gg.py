import pygame
import math
import random

# Initialize Pygame
pygame.init()

Fps = 60
winWidth, winHeight = 1000, 600
Width, Height = 600, 500
Rows, Column = 4, 4

RectHeight = Height // Rows
RectWidth = Width // Column

OutlineColor = (187, 173, 160)
BackgroundColor = (205, 192, 180)
FontColor = (119, 110, 101)
ThickOutline = 5

# Calculate offsets to center the grid
xOffset = (winWidth - Width) // 2
yOffset = (winHeight - Height) // 2

Window = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption("2048")

font = pygame.font.SysFont("comicsans", 40, bold=True)
moveVel = 20


class Tile:
    COLORS = [
        (237, 229, 218),
        (238, 225, 201),
        (243, 178, 122),
        (246, 150, 101),
        (247, 124, 95),
        (247, 95, 59),
        (237, 208, 115),
        (237, 204, 99),
        (236, 202, 80),
    ]

    def __init__(self, row, column, value):
        self.row = row
        self.column = column
        self.value = value
        self.x = xOffset + column * RectWidth
        self.y = yOffset + row * RectHeight
        self.width = RectWidth
        self.height = RectHeight

    def getColor(self):
        colorIndex = int(math.log2(self.value)) - 1
        color = self.COLORS[colorIndex]
        return color

    def draw(self, window):
        color = self.getColor()
        pygame.draw.rect(
            window,
            color,
            (self.x, self.y, self.width, self.height),
        )
        text = font.render(str(self.value), 1, FontColor)
        window.blit(
            text,
            (
                self.x + (self.width / 2 - text.get_width() / 2),
                self.y + (self.height / 2 - text.get_height() / 2),
            ),
        )

    def setPos(self, ceil=False):
        if ceil:
            self.row = math.ceil((self.y - yOffset) / RectHeight)
            self.column = math.ceil((self.x - xOffset) / RectWidth)
        else:
            self.row = math.floor((self.y - yOffset) / RectHeight)
            self.column = math.floor((self.x - xOffset) / RectWidth)

    def move(self, delta):
        """ Move the tile by a specified delta (change in x and y coordinates). """
        self.x += delta[0]
        self.y += delta[1]


def drawGrid(window):
    for i in range(1, Rows):
        y = yOffset + i * RectHeight
        pygame.draw.line(Window, OutlineColor, (xOffset, y), (xOffset + Width, y), ThickOutline)
    for i in range(1, Column):
        x = xOffset + i * RectWidth
        pygame.draw.line(Window, OutlineColor, (x, yOffset), (x, yOffset + Height), ThickOutline)
    pygame.draw.rect(Window, OutlineColor, (xOffset, yOffset, Width, Height), ThickOutline)


def draw(Window, tiles):
    Window.fill(BackgroundColor)
    for tile in tiles.values():
        tile.draw(Window)
    drawGrid(Window)
    pygame.display.update()


def getRandomPos(tiles):
    available_positions = [
        (r, c)
        for r in range(Rows)
        for c in range(Column)
        if f"{r},{c}" not in tiles
    ]
    if not available_positions:
        return None
    return random.choice(available_positions)


def genTile():
    tiles = {}
    for _ in range(2):
        pos = getRandomPos(tiles)
        if pos is None:
            break
        row, column = pos
        tiles[f"{row},{column}"] = Tile(row, column, 2)
    return tiles


def moveTiles(window, tiles, clock, direction):
    updated = True
    blocks = set()

    if direction == "left":
        sortFun = lambda x: x.column
        reverse = False
        delta = (-moveVel, 0)
        boundaryCheck = lambda tile: tile.column == 0
        getNextTile = lambda tile: tiles.get(f"{tile.row},{tile.column - 1}")
        mergeCheck = lambda tile, nextTile: tile.x > nextTile.x + moveVel
        moveCheck = lambda tile, nextTile: tile.x > nextTile.x + RectWidth + moveVel
        ceil = True
    elif direction == "right":
        sortFun = lambda x: x.column
        reverse = True
        delta = (moveVel, 0)
        boundaryCheck = lambda tile: tile.column == Column - 1
        getNextTile = lambda tile: tiles.get(f"{tile.row},{tile.column + 1}")
        mergeCheck = lambda tile, nextTile: tile.x < nextTile.x - moveVel
        moveCheck = lambda tile, nextTile: tile.x + RectWidth + moveVel < nextTile.x
        ceil = False
    elif direction == "up":
        sortFun = lambda x: x.row
        reverse = False
        delta = (0, -moveVel)
        boundaryCheck = lambda tile: tile.row == 0
        getNextTile = lambda tile: tiles.get(f"{tile.row - 1},{tile.column}")
        mergeCheck = lambda tile, nextTile: tile.y > nextTile.y + moveVel
        moveCheck = lambda tile, nextTile: tile.y > nextTile.y + RectHeight + moveVel
        ceil = True
    else:  # down
        sortFun = lambda x: x.row
        reverse = True
        delta = (0, moveVel)
        boundaryCheck = lambda tile: tile.row == Rows - 1
        getNextTile = lambda tile: tiles.get(f"{tile.row + 1},{tile.column}")
        mergeCheck = lambda tile, nextTile: tile.y < nextTile.y - moveVel
        moveCheck = lambda tile, nextTile: tile.y  + RectHeight + moveVel < nextTile.y
        ceil = False

    while updated:
        updated = False
        clock.tick(Fps)
        sortedTiles = sorted(tiles.values(), key=sortFun, reverse=reverse)

        for i, tile in enumerate(sortedTiles):
            if boundaryCheck(tile):
                continue
            nextTile = getNextTile(tile)
            if not nextTile:
                tile.move(delta)
            elif (tile.value == nextTile.value and
                  nextTile not in blocks and
                  tile not in blocks):
                if mergeCheck(tile, nextTile):
                    tile.move(delta)
                else:
                    nextTile.value *= 2
                    tiles.pop(f"{tile.row},{tile.column}")
                    blocks.add(nextTile)
                    continue
            elif moveCheck(tile, nextTile):
                tile.move(delta)
            else:
                continue

            tile.setPos(ceil)
            updated = True

        updateTiles(window, tiles, list(tiles.values()))

    return endMove(tiles)


def endMove(tiles):
    if len(tiles) == Rows * Column:
        return "lost"
    pos = getRandomPos(tiles)
    if pos:
        row, column = pos
        tiles[f"{row},{column}"] = Tile(row, column, random.choice([2, 4]))
    return "continue"


def updateTiles(window, tiles, sortedTiles):
    tiles.clear()
    for tile in sortedTiles:
        tiles[f"{tile.row},{tile.column}"] = tile
    draw(window, tiles)


def main(window):
    clock = pygame.time.Clock()
    run = True
    tiles = genTile()
    while run:
        clock.tick(Fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moveTiles(window, tiles, clock, "left")
                elif event.key == pygame.K_RIGHT:
                    moveTiles(window, tiles, clock, "right")
                elif event.key == pygame.K_UP:
                    moveTiles(window, tiles, clock, "up")
                elif event.key == pygame.K_DOWN:
                    moveTiles(window, tiles, clock, "down")

        draw(Window, tiles)
    pygame.quit()


if __name__ == "__main__":
    main(Window)
