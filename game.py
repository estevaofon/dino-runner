import pygame
import sys
from pyanimation import Animation
import random
import time

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
surface = pygame.Surface(screen.get_size())
surface = surface.convert()
surface.fill((255,255,255))
clock = pygame.time.Clock()

rex = Animation("rex_alfa.png")
rex.create_animation(0, 110, 50, 57, "run", duration=120, rows=1, cols=2)
rex.x = 150
rex.y = 260
screen.blit(surface, (0, 0))

# cloud
sprite = pygame.image.load("rex_alfa.png").convert()
crop_rect = (470, 5, 50, 25)
cloud1 = sprite.subsurface(crop_rect)
clouds_positions = [[random.randint(400, 600), random.randint(20,200)] for i in range(10)]

crop_rect = (20, 268, 540, 20)
terrain = sprite.subsurface(crop_rect)
terrains = [0, 480, 960]

crop_rect = (148, 55, 60, 48)
cactus = sprite.subsurface(crop_rect)
cactus_posx = [600, 900]
def s(s0,v0,a,t):
    return s0 + v0*t + (1/2)*a*t**2 
jump = False
gravity = 5
time1 = time.time()
velocidade = 100

if __name__ == '__main__':
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    time1 = time.time()
                    velocidade = -35
                    rex.y = 248
                  
        t =  time.time() - time1
        #print(t)
        if velocidade < 100 and rex.y <= 248: 
            rex.y += (int(velocidade*t)) 
            velocidade += gravity*t
        
        surface.fill((255,255,255))
        screen.blit(surface, (0,0))
        
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

        for i, posx in enumerate(cactus_posx):
            cactus_posx[i] -= 5
            screen.blit(cactus, (posx,258))
            if posx < 100:
                cactus_posx[i] = random.randint(800, 1500)
                 
        screen.blit(rex.update_surface(), (rex.x, rex.y))
        rex.run("run")
        #pygame.display.flip()
        pygame.display.update()
        clock.tick(60)
