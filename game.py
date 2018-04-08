import pygame
import sys
from pyanimation import Animation
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
surface = pygame.Surface(screen.get_size())
surface = surface.convert()
surface.fill((255,255,255))
clock = pygame.time.Clock()

rex = Animation("rex.png")
rex.create_animation(0, 110, 50, 57, "run", duration=120, rows=1, cols=2)
rex.x = 150
rex.y = 248
screen.blit(surface, (0, 0))

# cloud
sprite = pygame.image.load("rex.png").convert()
crop_rect = (470, 5, 50, 25)
cloud1 = sprite.subsurface(crop_rect)
clouds_positions = [[random.randint(400, 600), random.randint(20,200)] for i in range(10)]

crop_rect = (20, 268, 540, 20)
terrain = sprite.subsurface(crop_rect)
terrains = [0, 480, 960]

if __name__ == '__main__':
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    rex.y = rex.y - 50

        surface.fill((255,255,255))
        screen.blit(surface, (0,0))
        clock.tick(60)
        for i, terrain_posx in enumerate(terrains):
            screen.blit(terrain, (terrain_posx,300))
            terrains[i] -=3
            if terrain_posx < -500:
                terrains[i]=960

        for i, cloud_pos in enumerate(clouds_positions):
            screen.blit(cloud1, cloud_pos)
            clouds_positions[i][0] -=2
            if clouds_positions[i][0] < 0:
                clouds_positions[i][0]= random.randint(800, 1200)
                clouds_positions[i][1] = random.randint(20, 200)
    
        screen.blit(rex.update_surface(), (rex.x, rex.y))
        rex.run("run")
        pygame.display.flip()
        pygame.display.update()
