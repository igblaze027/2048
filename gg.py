import pygame
import math
import random

# Initialize Pygame
pygame.init()


Fps = 60

Width, Height = 800, 500
Rows, Column = 4 ,4

RectHeight  = Height // Rows
RectWidth = Width // Column

OutlineColor = (187, 173, 160)
BackgroundColor = (205,192, 180)
FontColor = (119, 110, 101)
ThickOutline = 10

Window = pygame.display.set_mode((Width, Height))

pygame.display.set_caption("2048")

font = pygame.font.SysFont("comicsans", 40, bold = True)
moveVel = 20

def draw(Window):
    Window.fill(BackgroundColor, )
    pygame.display.update()

def main(window):
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(Fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        draw(Window)
    pygame.quit()














if __name__ == "__main__":
    main(Window)