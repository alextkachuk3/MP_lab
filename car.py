import pygame
import os
import math


class Car:
    def __init__(self, window_width, window_height, x, y):
        car_width_coefficient = 0.34
        car_height_coefficient = 0.32
        self.window_width = window_width
        self.window_height = window_height
        self.car_width = window_width * car_width_coefficient
        self.car_height = window_height * car_height_coefficient
        self.sprite = pygame.image.load(os.path.join('images', 'car.png'))
        self.sprite = pygame.transform.smoothscale(self.sprite, (self.car_width, self.car_height))
        self.sprite_rotated = self.sprite
        self.x = x
        self.y = y
        self.speed = 0
        self.angle = 0
        self.acceleration = 0.0004
        self.turn_speed = 0.001
        self.forward_count = 0
        self.backward_count = 0
        self.max_forward_count = 350
        self.max_backward_count = 350
        self.rotated_rectangle = self.sprite_rotated.get_rect(center=(round(self.x), round(self.y)))
        self.window_rectangle = pygame.Rect(0, 0, window_width, window_height)

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0
        self.angle = 0
        self.forward_count = 0
        self.backward_count = 0
        self.rotated_rectangle = self.sprite_rotated.get_rect(center=(round(self.x), round(self.y)))

    def blit(self, surface: pygame.Surface):
        surface.blit(self.sprite_rotated, self.rotated_rectangle)

    def no_action(self):
        if self.backward_count > 0:
            self.backward_count -= 1
        if self.forward_count > 0:
            self.forward_count -= 1
        self.update_position()

    def forward(self):
        if self.backward_count > 0:
            self.backward_count = max(self.backward_count - 1, 0)
        else:
            self.forward_count = min(self.forward_count + 1, self.max_forward_count)
        self.update_position()

    def forward_left(self):
        self.forward()
        self.left()

    def forward_right(self):
        self.forward()
        self.right()

    def backward(self):
        if self.forward_count > 0:
            self.forward_count = max(self.forward_count - 1, 0)
        else:
            self.backward_count = min(self.backward_count + 1, self.max_backward_count)
        self.update_position()

    def backward_left(self):
        self.backward()
        self.left()

    def backward_right(self):
        self.backward()
        self.right()

    def left(self):
        self.angle += self.turn_speed * max(self.forward_count, self.backward_count)
        self.update_position()

    def right(self):
        self.angle -= self.turn_speed * max(self.forward_count, self.backward_count)
        self.update_position()

    def update_position(self):
        if self.forward_count > 0:
            self.speed = self.forward_count ** 1.3 * self.acceleration
        elif self.backward_count > 0:
            self.speed = self.backward_count ** 1.3 * -self.acceleration
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y -= self.speed * math.sin(math.radians(self.angle))
        if self.angle > 180:
            self.angle = -180
        elif self.angle < -180:
            self.angle = 180
        self.sprite_rotated = pygame.transform.rotate(self.sprite, self.angle)
        self.rotated_rectangle = self.sprite_rotated.get_rect(center=(round(self.x), round(self.y)))

    def check_border_collision(self):

        car_rect = self.sprite_rotated.get_rect(center=(round(self.x), round(self.y)))
        if not self.window_rectangle.contains(car_rect):
            return True
        return False
