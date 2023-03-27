import pygame
import os
import math


class Car:
    def __init__(self, window_width, window_height, x, y):
        car_width_coefficient = 0.28
        car_height_coefficient = 0.27
        self.car_width = window_width * car_width_coefficient
        self.car_height = window_height * car_height_coefficient
        self.sprite = pygame.image.load(os.path.join('images', 'car.png'))
        self.sprite = pygame.transform.smoothscale(self.sprite, (self.car_width, self.car_height))
        self.sprite_rotated = self.sprite
        self.x = x
        self.y = y
        self.speed = 0
        self.angle = 0
        self.max_speed = 0.8
        self.min_speed = -0.7
        self.acceleration = 0.5
        self.friction = 0.1
        self.turn_speed = 0.5
        self.rotated_rectangle = self.sprite_rotated.get_rect(center=(round(self.x), round(self.y)))

    def blit(self, surface: pygame.Surface):
        surface.blit(self.sprite_rotated, self.rotated_rectangle)

    def forward(self):
        self.speed = min(self.speed + self.acceleration, self.max_speed)
        self.update_position()

    def backward(self):
        self.speed = max(self.speed - self.acceleration, self.min_speed)
        self.update_position()

    def left(self):
        self.angle += self.turn_speed
        self.update_position()

    def right(self):
        self.angle -= self.turn_speed
        self.update_position()

    def update_position(self):
        self.speed = max(self.speed - self.friction, 0) if self.speed > 0 else min(self.speed + self.friction, 0)
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y -= self.speed * math.sin(math.radians(self.angle))
        if self.angle > 180:
            self.angle = -180
        elif self.angle < -180:
            self.angle = 180
        self.sprite_rotated = pygame.transform.rotate(self.sprite, self.angle)
        self.rotated_rectangle = self.sprite_rotated.get_rect(center=(round(self.x), round(self.y)))
