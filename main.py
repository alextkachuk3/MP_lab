import pygame

from road import Road

window_width = 1000
window_height = 600

pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Вжух вжух')

road = Road(window_width, window_height, 7)
road.blit(screen)

running = True

while running:
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
