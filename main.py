import pygame
import os

from road import Road

window_width = 1000
window_height = 600

pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Вжух вжух')

road = Road(window_width, window_height, 7)
road.blit(screen)

picture = pygame.image.load(os.path.join('images', 'car.png'))
picture = pygame.transform.smoothscale(picture, (300, 150))


running = True

while running:
    screen.blit(picture, (100, 375))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
