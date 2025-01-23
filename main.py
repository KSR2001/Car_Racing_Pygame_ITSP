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

def rotating_img(pywin, img, pos, angle):
    pywin.blit(
        pygame.transform.rotate(img, angle),
        pygame.transform.rotate(img, angle).get_rect(
            center=img.get_rect(topleft=pos).center
        ).topleft
    )


class Main_Car:
    IMG = None
    start_position = (0,0)

    def __init__(self, car_speed, car_rotation_speed):
        self.car_rotation_speed = car_rotation_speed
        self.acc = 0.1
        self.img = self.IMG
        self.angle = 0
        self.hor, self.ver = self.start_position
        self.car_speed = car_speed
        self.speed = 0

    def draw(self, win):
        rotating_img(win, self.img, (self.hor, self.ver), self.angle)

    def forward_moving(self):
        self.speed = min(self.speed + self.acc, self.car_speed)
        self.move()

    def backward_moving(self):
        self.speed = max(self.speed - self.acc, -self.car_speed/2)
        self.move()

    def speed_reduction(self):
        self.speed = max(self.speed - self.acc / 2, 0)
        self.move()

    def rotating_car(self, move_left=False, move_right=False):
        actions = {
            (True, False): lambda: self.angle + self.car_rotation_speed,
            (False, True): lambda: self.angle - self.car_rotation_speed,
        }
        self.angle = actions.get((move_left, move_right), lambda: self.angle)()

    def move(self):
        radians = math.radians(self.angle)
        vertical, horizontal = math.cos(radians) * self.speed, math.sin(radians) * self.speed
        self.ver -= vertical
        self.hor -= horizontal

    def bounce_back(self):
        self.speed = -self.speed
        self.move()

    def collide(self, mask, x=0, y=0):
        car_collision_mask = pygame.mask.from_surface(self.img)
        collision_offset = (int(self.hor - x), int(self.ver - y))
        point_of_intersection = mask.overlap(car_collision_mask, collision_offset)
        return point_of_intersection

    def reset(self):
        self.hor, self.ver = self.start_position
        self.angle = 0
        self.speed = 0

class Car1(Main_Car):
    IMG = RED_CAR
    start_position = (20, 445)

class Car2(Main_Car):
    IMG = YELLOW_CAR
    start_position = (60, 450)

def draw(win, game_images, player_car_1, player_car_2, process_game):
    for image, position in game_images:
        win.blit(image, position)
    txt_level = SMALL_FONT.render(f"Level {process_game.level}", 1, (255, 255, 255))
    win.blit(txt_level, (30, HEIGHT - txt_level.get_height() - 70))
    player_car_1.draw(win)
    player_car_2.draw(win)
    pygame.display.update()


def moving_cars(player_car_1, player_car_2):
    storing_keys = pygame.key.get_pressed()
    if storing_keys[pygame.K_q]:
        sound.play()
    if storing_keys[pygame.K_e]:
        sound.stop()
    if storing_keys[pygame.K_n]:
        pygame.quit()
    if storing_keys[pygame.K_m]:
        process_game.game_reset()
        player_car_1.reset()
        player_car_2.reset()
    car1_moved = False
    if storing_keys[pygame.K_a]:
        player_car_1.rotating_car(move_left=True)
    if storing_keys[pygame.K_d]:
        player_car_1.rotating_car(move_right=True)
    if storing_keys[pygame.K_w]:
        car1_moved = True
        player_car_1.forward_moving()
    if storing_keys[pygame.K_s]:
        car1_moved = True
        player_car_1.backward_moving()
    if not car1_moved:
        player_car_1.speed_reduction()
    car2_moved = False
    if storing_keys[pygame.K_LEFT]:
        player_car_2.rotating_car(move_left=True)
    if storing_keys[pygame.K_RIGHT]:
        player_car_2.rotating_car(move_right=True)
    if storing_keys[pygame.K_UP]:
        car2_moved = True
        player_car_2.forward_moving()
    if storing_keys[pygame.K_DOWN]:
        car2_moved = True
        player_car_2.backward_moving()
    if not car2_moved:
        player_car_2.speed_reduction()

def cars_collision(player_car_1, player_car_2, process_game):
    car_1_finish = player_car_1.collide(finish_line_1_mask, *finish_1_pos)
    if car_1_finish != None:
        process_game.add_point("Player 1")
        process_game.lev_change()
        player_car_1.reset()
        player_car_2.reset()
    car_2_finish = player_car_2.collide(finish_line_1_mask, *finish_1_pos)
    if car_2_finish != None:
        process_game.add_point("Player 2")
        process_game.lev_change()
        player_car_1.reset()
        player_car_2.reset()
    if player_car_1.collide(path_border_mask) != None:
        player_car_1.bounce_back()
    if player_car_2.collide(path_border_mask) != None:
        player_car_2.bounce_back()

def draw_trophy(win, trophy, text_y_position):
    trophy_x = win.get_width() / 2 - trophy.get_width() / 2
    trophy_y = text_y_position + 50
    win.blit(trophy, (trophy_x, trophy_y))
    pygame.display.update()

class process:
    Tot_Levels = 3
    def __init__(self, level=1):
        self.level = level
        self.game_start = False
        self.scores = {"Player 1": 0, "Player 2": 0}

    def lev_change(self):
        self.level += 1
        self.game_start = False

    def game_reset(self):
        self.level = 1
        self.game_start = False
        self.scores = {"Player 1": 0, "Player 2": 0}

    def game_finish(self):
        return self.level > self.Tot_Levels

    def starting_level(self):
        self.game_start = True

    def add_point(self, player):
        self.scores[player] += 1

    def get_winner(self):
        if self.scores["Player 1"] > self.scores["Player 2"]:
            return (f"Player 1 (Red) Wins! \n Player 1 score ={self.scores['Player 1']}\n "
                    f"Player 2 score ={self.scores['Player 2']}")
        if self.scores["Player 1"] < self.scores["Player 2"]:
            return (f"Player 2 (Yellow) Wins! \n Player 1 score ={self.scores['Player 1']}\n "
                    f"Player 2 score ={self.scores['Player 2']}")


player_car_1 = Car1(2, 2)
player_car_2 = Car2(2, 2)
game_images = [(Dirt, (0, 0)), (PATH, (0, 0)),
          (finish_line_1, finish_1_pos), (finish_line_2, (20,420)), (path_border, (0, 0)), (plant1, (100, 380)),
          (plant2, (5, 210)), (plant3, (250,180)), (plant4, (400,90)), (cat, (1, 3))]
process_game = process()
Myclock = pygame.time.Clock()
Frames = 60
running_game = True
while running_game:
    Myclock.tick(Frames)
    draw(WIN, game_images, player_car_1, player_car_2, process_game)
    while not process_game.game_start:
        instructions_text = (
            f"Press any key to start level {process_game.level}!\n"
            f"{'Instructions:'.center(40)}\n"
            f"Player 1 (Red Car) must use W/A/S/D to move\n"
            f"Player 2 (Yellow Car) must use Arrow Keys to move\n"
            f" Use Q to play 'GAME SOUND' and E to stop playing it\n"
            f" Use N to 'QUIT' the game and M to 'RESET' it\n"
            f"There are 3 levels in the game\n"
            f"The player who wins the most levels is the WINNER!\n"
            f"HINT: MAKE GOOD TURNS! "
        )
        draw_instructions(WIN, SMALL_FONT, instructions_text)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            if event.type == pygame.KEYDOWN:
                process_game.starting_level()

