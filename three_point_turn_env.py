import gym
import numpy as np
from gym.spaces import Discrete, Box, Tuple
from stable_baselines3 import PPO, DQN
from stable_baselines3.common.evaluation import evaluate_policy

import pygame

from car import Car
from road import Road

window_width = 1000
window_height = 600


class ThreePointTurnEnv(gym.Env):
    def __init__(self):
        self.road = Road(window_width, window_height, 7)
        self.car = Car(window_width, window_height, 100, 450)
        self.action_space = Discrete(4)
        # self.observation_space = Tuple((Box(low=np.array([-180.0]), high=np.array([180.0])),
        #                                 Box(low=np.array([0]), high=np.array([1000])),
        #                                 Box(low=np.array([0]), high=np.array([600]))))
        self.observation_space = Box(low=np.array([-180.0]), high=np.array([180.0]))
        self.length = 5000
        self.prev_angle = 0

    def step(self, action):
        if action == 0:
            self.car.left()
        elif action == 1:
            self.car.right()
        elif action == 2:
            self.car.forward()
        elif action == 3:
            self.car.backward()

        # if self.car.angle < -179.5 or self.car.angle > 179.5:
        #     reward = 1
        # elif self.car.angle < -160 or self.car.angle > 160:
        #     reward = 0.8
        # elif self.car.angle < -120 or self.car.angle > 120:
        #     reward = 0.1
        # elif self.car.angle < -90 or self.car.angle > 90:
        #     reward = -0.1
        # elif self.car.angle < -60 or self.car.angle > 60:
        #     reward = -0.8
        # elif self.car.angle < -30 or self.car.angle > 30:
        #     reward = -0.9
        # else:
        #     reward = -1

        # if self.car.angle < 0:
        #     reward = -self.car.angle / 180
        # else:
        #     reward = self.car.angle / 180

        # if self.car.angle < 0:
        #     if self.prev_angle > self.car.angle:
        #         reward = 1
        #     else:
        #         reward = -1
        # else:
        #     if self.prev_angle < self.car.angle:
        #         reward = 1
        #     else:
        #         reward = -1

        reward = self.car.angle - self.prev_angle

        self.prev_angle = self.car.angle

        self.length -= 1

        if self.length <= 0:
            done = True
        else:
            done = False

        info = {}

        # return Tuple(([self.car.angle], [self.car.x], [self.car.y])), reward, done, info
        return self.car.angle, reward, done, info

    def render(self, mode):
        if mode == 'human':
            self.road.blit(screen)
            self.car.blit(screen)
            pygame.display.update()

    def reset(self):
        self.prev_angle = 0
        self.length = 5000
        self.car.x = 100
        self.car.y = 450
        self.car.angle = 0
        self.car.speed = 0
        return self.car.angle


pygame.init()

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Вжух вжух')

env = ThreePointTurnEnv()

model = DQN("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=100000)
model.save('PPO')
evaluate_policy(model, env, n_eval_episodes=10, render=True)
