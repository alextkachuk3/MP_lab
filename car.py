import pygame
import os


class Car:
    def __init__(self, window_width, window_height, x, y):
        car_width_coefficient = 0.3
        car_height_coefficient = 0.3
        self.car_width = window_width * car_width_coefficient
        self.car_height = window_height * car_height_coefficient
        self.sprite = pygame.image.load(os.path.join('images', 'car.png'))
        self.sprite = pygame.transform.smoothscale(self.sprite, (self.car_width, self.car_height))
        self.x = x
        self.y = y

    def blit(self, surface: pygame.Surface):
        surface.blit(self.sprite, (self.x, self.y))
