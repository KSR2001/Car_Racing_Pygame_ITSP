import pygame
import math
pygame.font.init()
pygame.init()
pygame.mixer.init()


def img_adjust(myimg, resize):
    a = round(myimg.get_width() * resize)
    b = round(myimg.get_height() * resize)
    size = a,b
    return pygame.transform.scale(myimg, size)

Dirt = img_adjust(pygame.image.load("GameImgs/Dirt.jpg"), 2.5)
PATH = img_adjust(pygame.image.load("GameImgs/path.png"), 0.9)
path_border = img_adjust(pygame.image.load("GameImgs/path_border.png"), 0.9)
path_border_mask = pygame.mask.from_surface(path_border)
plant1 = img_adjust(pygame.image.load("GameImgs/plant1.png"), 0.20)
plant2 = img_adjust(pygame.image.load("GameImgs/plant2.png"), 0.10)
plant3 = img_adjust(pygame.image.load("GameImgs/plant3.png"), 0.30)
plant4 = img_adjust(pygame.image.load("GameImgs/plant4.png"), 0.10)
trophy = img_adjust(pygame.image.load("GameImgs/trophy.png"), 0.40)
cat = img_adjust(pygame.image.load("GameImgs/cat.png"), 0.17)
finish_line_1 = pygame.image.load("GameImgs/finish_line1.png")
finish_line_1_mask = pygame.mask.from_surface(finish_line_1)
finish_1_pos = (330, 25)
finish_line_2 = pygame.image.load("GameImgs/finish_line2.png")
RED_CAR = img_adjust(pygame.image.load("GameImgs/red_car.png"), 0.15)
YELLOW_CAR = img_adjust(pygame.image.load("GameImgs/yellow_car.png"), 0.10)
WIDTH = PATH.get_width()
HEIGHT = PATH.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiplayer Car Racing Game!")
sound = pygame.mixer.Sound("GameImgs/sound_NCS.OGG")
SMALL_FONT = pygame.font.SysFont("comicsans", 15)

def draw_instructions(win, font, instructions_text, background_color=(0, 0, 0, 150), text_color=(255, 255, 255)):
    text_lines = instructions_text.split("\n")
    text_width = max(font.size(line)[0] for line in text_lines) + 20
    text_height = sum(font.size(line)[1] for line in text_lines) + 20
    text_x = (win.get_width() - text_width) / 2
    text_y = (win.get_height() - text_height) / 2

    box_surface = pygame.Surface((text_width, text_height), pygame.SRCALPHA)
    box_surface.fill(background_color)
    win.blit(box_surface, (text_x, text_y))

    start_y = text_y + 10
    for line in text_lines:
        render = font.render(line, 1, text_color)
        win.blit(render, (win.get_width() / 2 - render.get_width() / 2, start_y))
        start_y += render.get_height()




