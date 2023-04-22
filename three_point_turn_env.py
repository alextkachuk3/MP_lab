import gym
import numpy as np
from gym.spaces import Discrete, Box, Dict
# from gym.utils.env_checker import check_env
from stable_baselines3 import PPO, DQN
from stable_baselines3.common.evaluation import evaluate_policy

import pygame

from car import Car
from road import Road

window_width = 1000
window_height = 600

render = True


class ThreePointTurnEnv(gym.Env):
    def __init__(self):
        self.road = Road(window_width, window_height, 7)
        self.car = Car(window_width, window_height, 230, 450)
        self.action_space = Discrete(7)

        self.observation_space = Dict({'angle': Box(low=np.array([-180.0]), high=np.array([180.0])),
                                       'x': Box(low=np.array([0]), high=np.array([1000.0])),
                                       'y': Box(low=np.array([0]), high=np.array([600.0]))})
        self.prev_angle = None
        self.prev_x = None
        self.prev_y = None
        self.length = None
        self.screen = None
        self.total_reward = None

        self.checkpoint_angle = None
        self.checkpoint_y = None
        self.checkpoint_x = None
        self.checkpoint_total_reward = None
        self.checkpoint_length = None
        self.checkpoint_backward = None
        self.checkpoint_forward = None
        self.check_point = 0

        self.full_reset()

        if render:
            self.init_render()

    def step(self, action):
        self.length -= 1

        self.prev_angle = self.car.angle
        self.prev_x = self.car.x
        self.prev_y = self.car.y
        self.prev_border_distance = self.car.distance_to_border()

        if action == 0:
            self.car.no_action()
        elif action == 1:
            self.car.forward_left()
        elif action == 2:
            self.car.forward()
        elif action == 3:
            self.car.forward_right()
        elif action == 4:
            self.car.backward_right()
        elif action == 5:
            self.car.backward()
        elif action == 6:
            self.car.backward_left()

        if self.car.check_border_collision():
            reward = -100000
            self.length = 0
        else:
            # reward = (self.prev_x - self.car.x) * 100 + (self.prev_y - self.car.y) * 400 + (self.car.angle - self.prev_angle) * 400
            reward = (self.prev_x - self.car.x) * 50 + (self.prev_y - self.car.y) * 450 + (self.car.angle - self.prev_angle) * 700 - (self.prev_border_distance - self.car.distance_to_border()) * 900

            # reward = (self.car.x - self.prev_x) * 100

        self.total_reward += reward

        if self.length <= 0:
            done = True
        else:
            done = False

        if self.car.angle > 65 and self.check_point == 0 and 320 > self.car.y > 310:
            self.check_point = 1
            self.save_checkpoint()

        info = {}

        if render:
            self.render(mode='human')

        return {'angle': [self.car.angle], 'x': [self.car.x], 'y': [self.car.y]}, reward, done, info

    def render(self, mode):
        if mode == 'human':
            pygame.event.get()
            self.road.blit(self.screen)
            self.car.blit(self.screen)
            pygame.display.update()

    def reset(self):
        print(self.check_point)
        print(self.total_reward)
        if self.check_point == 0:
            self.full_reset()
        elif self.check_point == 1:
            self.load_checkpoint()
        return {'angle': self.car.angle, 'x': self.car.x, 'y': self.car.y}

    def full_reset(self):
        self.total_reward = 0
        self.length = 4500
        self.car.reset(230, 450)
        self.prev_x = self.car.x
        self.prev_y = self.car.y
        self.prev_angle = self.car.angle

    def save_checkpoint(self):
        self.checkpoint_length = self.length
        self.checkpoint_total_reward = self.total_reward
        self.checkpoint_x = self.car.x
        self.checkpoint_y = self.car.y
        self.checkpoint_angle = self.car.angle
        self.checkpoint_forward = self.car.forward_count
        self.checkpoint_backward = self.car.backward_count

    def load_checkpoint(self):
        self.length = self.checkpoint_length
        self.total_reward = self.checkpoint_total_reward
        self.car.x = self.checkpoint_x
        self.car.y = self.checkpoint_y
        self.car.angle = self.checkpoint_angle
        self.car.forward_count = self.checkpoint_forward
        self.car.backward_count = self.checkpoint_backward

    def init_render(self):
        pygame.init()
        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption('Вжух вжух')


env = ThreePointTurnEnv()
# check_env(env)

load = True
train = False

if load:
    model = DQN.load('DQN')
else:
    model = DQN("MultiInputPolicy", env, verbose=1, tensorboard_log='tb_dqn')

if train:
    model.learn(total_timesteps=300000)
    model.save('DQN')

if render:
    evaluate_policy(model, env, n_eval_episodes=10, render=True)
