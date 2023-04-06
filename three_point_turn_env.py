import gym
import numpy as np
from gym.spaces import Discrete, Box, Dict
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
        self.car = Car(window_width, window_height, 230, 450)
        self.action_space = Discrete(6)

        self.observation_space = Dict({'angle': Box(low=np.array([-180.0]), high=np.array([180.0])),
                                       'x': Box(low=np.array([-2000.0]), high=np.array([4000.0])),
                                       'y': Box(low=np.array([-1500.0]), high=np.array([3000.0]))})
        self.prev_angle = None
        self.length = None


        self.reset()

    def step(self, action):
        if action == 0:
            self.car.forward_left()
        elif action == 1:
            self.car.forward()
        elif action == 2:
            self.car.forward_right()
        elif action == 3:
            self.car.backward_right()
        elif action == 4:
            self.car.backward()
        elif action == 5:
            self.car.backward_left()

        if self.car.check_border_collision():
            reward = -100.0
        else:
            reward = self.car.angle - self.prev_angle * 180

        self.prev_angle = self.car.angle

        self.length -= 1

        if self.length <= 0:
            done = True
        else:
            done = False

        info = {}

        return {'angle': self.car.angle, 'x': self.car.x, 'y': self.car.y}, reward, done, info

    def render(self, mode):
        if mode == 'human':
            pygame.event.get()
            self.road.blit(screen)
            self.car.blit(screen)
            pygame.display.update()

    def reset(self):
        self.prev_angle = 0
        self.length = 1500
        self.car.x = 230
        self.car.y = 450
        self.car.angle = 0
        self.car.speed = 0
        return {'angle': self.car.angle, 'x': self.car.x, 'y': self.car.y}


env = ThreePointTurnEnv()

load = False
render = True

if load:
    model = DQN.load('DQN')

else:
    model = DQN("MultiInputPolicy", env, verbose=1)
    model.learn(total_timesteps=100000)
    model.save('DQN')

if render:
    pygame.init()

    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('Вжух вжух')
    evaluate_policy(model, env, n_eval_episodes=3, render=render)
