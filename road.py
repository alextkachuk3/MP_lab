import pygame


class Road:
    def __init__(self, window_width, window_height, lines_count):
        road_line_height_percent = 0.04
        line_begin_pos_x_coefficient = 5
        space_between_x_coefficient = 1 / lines_count
        self.line_width = window_width / lines_count
        self.line_height = window_height * road_line_height_percent
        self.line_pos_x = -window_width / 5 + window_width / lines_count

        cur_line_pos_x = -window_width / line_begin_pos_x_coefficient + window_width / lines_count
        self.line_pos_y = window_height * 0.5 - self.line_height * 0.5
        self.lines_pos_x = []

        for i in range(0, lines_count):
            self.lines_pos_x.append(cur_line_pos_x)
            cur_line_pos_x = cur_line_pos_x + self.line_width + window_width / lines_count * space_between_x_coefficient

    def blit(self, surface: pygame.Surface):
        surface.fill('Black')
        for line_pos_x in self.lines_pos_x:
            line = pygame.Surface((self.line_width, self.line_height))
            line.fill('White')
            surface.blit(line, (line_pos_x, self.line_pos_y))
