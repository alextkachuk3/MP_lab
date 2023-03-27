import pygame

window_width = 1000
window_height = 600

pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Вжух вжух')

road_lines_count = 7
road_line_height_percent = 0.04
line_width = window_width / road_lines_count
line_height = window_height * road_line_height_percent
line_begin_pos_x_coefficient = 5
space_between_x_coefficient = 0.125
line_pos_x = -window_width / line_begin_pos_x_coefficient + window_width / road_lines_count

for i in range(0, road_lines_count):
    line = pygame.Surface((line_width, line_height))
    line.fill('White')
    screen.blit(line, (line_pos_x, window_height * 0.5 - line_height * 0.5))
    line_pos_x = line_pos_x + line_width + window_width / road_lines_count * space_between_x_coefficient

running = True

while running:
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
