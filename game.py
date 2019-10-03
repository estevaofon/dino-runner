"""
Dino Runner Clone
"""

import pygame
import sys
from pyanimation import Animation
import random
import time
import os


class ScenarioElement():
    def __init__(self, sprite, crop_rect, coord_list):
        self.surface = sprite.subsurface(crop_rect)
        self.coord_list = coord_list


pygame.init()
pygame.mixer.init()

BASEDIR = os.path.dirname(os.path.abspath(__file__))
SCREEN_WIDTH, SCREEN_HEIGHT = (800, 400)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
surface = pygame.Surface(screen.get_size())
surface = surface.convert()
surface.fill((255, 255, 255))
clock = pygame.time.Clock()
screen.blit(surface, (0, 0))

# Rex Animation
rex_sprite_path = os.path.join(BASEDIR, "images/sprites", "rex_alfa.png")
rex = Animation(rex_sprite_path)
rex.create_animation(0, 110, 50, 57, "run", duration=120, rows=1, cols=2)
rex.x = 150
rex.y = 250

sprite = pygame.image.load(rex_sprite_path).convert()

cactus_posx = [600, 900]
cactus_list_coord = [[x, 258] for x in cactus_posx]
cactus_obj = ScenarioElement(sprite, (148, 55, 60, 48), cactus_list_coord)
terrain_posx = [0, 480, 960]
terrain_list_coord = [[x, 300] for x in terrain_posx]
terrain_obj = ScenarioElement(sprite, (20, 268, 540, 20), terrain_list_coord)
coord_list = [[random.randint(400, 600), random.randint(20, 200)] for i in range(10)]
cloud_obj = ScenarioElement(sprite, (470, 5, 50, 25), coord_list)

jump = False
gravity = 5
time1 = time.time()
velocidade = 100
jumping = False
game_speed = 1.3
pontos = 0
myfont = pygame.font.SysFont('Comic Sans MS', 30)
game_over = False
green = (0, 255, 0)
blue = (0, 0, 255)

sound_path = os.path.join(BASEDIR, "sound", "press.wav")
sounda = pygame.mixer.Sound(sound_path)


def move_element(scenario_obj, game_speed, game_speed_multiplicator,
                 x_limit, x_start, y_start):
    for i, coord in enumerate(scenario_obj.coord_list):
        screen.blit(scenario_obj.surface, coord)
        # coord x
        scenario_obj.coord_list[i][0] -= game_speed_multiplicator*game_speed
        if coord[0] < x_limit:
            scenario_obj.coord_list[i][0] = x_start
            scenario_obj.coord_list[i][1] = y_start


def check_collision_with_list(player_rect, obstacle_obj, color, obs_dx=0, obs_dy=0):
    for coord in obstacle_obj.coord_list:
        obstacle_rect = pygame.Rect(coord[0]+obs_dx,
                                    coord[1]+obs_dy, 50, 40)
        pygame.draw.rect(screen, color, obstacle_rect)
        if player_rect.colliderect(obstacle_rect):
            return True


def display_game_over():
    textsurface_over = myfont.render(f'Game Over', False, (0, 0, 0))
    screen.blit(textsurface_over, (350, 200))


def display_score():
    textsurface = myfont.render(f'{pontos:.0f}', False, (0, 0, 0))
    screen.blit(textsurface, (700, 0))


if __name__ == '__main__':
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if rex.y >= 250:
                        sounda.play()
                        time1 = time.time()
                        velocidade = -37
                        rex.y = 250

        t = time.time() - time1
        if velocidade < 100 and rex.y <= 250:
            rex.y += (int(velocidade*t))
            velocidade += gravity*t

        surface.fill((255, 255, 255))
        screen.blit(surface, (0, 0))
        rex_rect = pygame.Rect(rex.x+2, rex.y, 40, 60)
        pygame.draw.rect(screen, (255, 0, 0), rex_rect)

        if check_collision_with_list(rex_rect, cactus_obj, green, obs_dx=10, obs_dy=10):
            game_over = True
        if check_collision_with_list(rex_rect, cloud_obj, blue):
            game_over = True

        move_element(terrain_obj, game_speed, 3, -500, 960, terrain_obj.coord_list[0][1])
        move_element(cloud_obj, game_speed, 1, 0, random.randint(800, 1200),
                     random.randint(20, 200))
        move_element(cactus_obj, game_speed, 4, 100, random.randint(800, 1500),
                     cactus_obj.coord_list[0][1])

        if game_over:
            display_game_over()
        if not game_over:
            pontos += 0.5
        display_score()
        screen.blit(rex.update_surface(), (rex.x, rex.y))
        rex.run("run")
        pygame.display.update()
        clock.tick(60)
