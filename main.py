import pygame
import os

from car import Car
from road import Road

window_width = 1000
window_height = 600

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Вжух вжух')

road = Road(window_width, window_height, 7)

car = Car(window_width, window_height, 100, 450)

running = True

while running:
    clock.tick(120)
    road.blit(screen)
    car.blit(screen)
    pygame.display.update()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        car.forward()
    if keys[pygame.K_s]:
        car.backward()
    if keys[pygame.K_a]:
        car.left()
    if keys[pygame.K_d]:
        car.right()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
