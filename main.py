import pygame

from car import Car
from road import Road

window_width = 1000
window_height = 600

pygame.init()

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Вжух вжух')

road = Road(window_width, window_height, 7)

car = Car(window_width, window_height, 230, 450)

running = True
k = 0

while running:
    road.blit(screen)
    car.blit(screen)
    pygame.display.update()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and keys[pygame.K_a]:
        car.forward_left()
    elif keys[pygame.K_w] and keys[pygame.K_d]:
        car.forward_right()
    elif keys[pygame.K_w]:
        car.forward()
    elif keys[pygame.K_s] and keys[pygame.K_a]:
        car.backward_right()
    elif keys[pygame.K_s] and keys[pygame.K_d]:
        car.backward_left()
    elif keys[pygame.K_s]:
        car.backward()
    else:
        car.no_action()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    print("x={x} "
          "y={y} "
          "angle={angle} "
          "forward_count={forward_count} "
          "backward_count={backward_count}".format(x=str(car.x),
                                                   y=str(car.y),
                                                   angle=str(car.angle),
                                                   forward_count=str(car.forward_count),
                                                   backward_count=str(car.backward_count)))
    print("Distance to border {}".format(str(car.distance_to_border())))

    if car.check_border_collision():
        print("Collision detected! {k} ".format(k=str(k)))
        k = k + 1
