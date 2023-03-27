import pygame
import os

from car import Car
from road import Road

window_width = 1000
window_height = 600

pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Вжух вжух')

road = Road(window_width, window_height, 7)
road.blit(screen)

car = Car(window_width, window_height, 100, 375)

running = True

while running:
    car.blit(screen)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
