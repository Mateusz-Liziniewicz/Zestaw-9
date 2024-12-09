import sys
import random
import pygame
import time

def add_snake_segment(snake_body, direction, segment_size):
    last_segment = snake_body[-1]
    if direction == "u":
        new_segment = pygame.Rect(last_segment.x, last_segment.y + segment_size, segment_size, segment_size)
    elif direction == "d":
        new_segment = pygame.Rect(last_segment.x, last_segment.y - segment_size, segment_size, segment_size)
    elif direction == "l":
        new_segment = pygame.Rect(last_segment.x + segment_size, last_segment.y, segment_size, segment_size)
    elif direction == "r":
        new_segment = pygame.Rect(last_segment.x - segment_size, last_segment.y, segment_size, segment_size)
    snake_body.append(new_segment)
    return snake_body

def counting_score(c):
    c += 1
    return c

def game_over_screen(screen, screen_width, screen_height, c):
    screen.fill((255, 0, 0))
    font_big = pygame.font.Font(None, 100)
    font_med = pygame.font.Font(None, 80)
    font_small = pygame.font.Font(None, 50)
    text = font_big.render("GAME OVER!", True, (255, 255, 255))
    score = font_med.render(f"Score: {c}", True, (255, 255, 255))
    info = font_small.render("(space to continue)", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    text_scr = score.get_rect(center=(screen_width // 2, (screen_height // 2) + 100))
    text_inf = info.get_rect(center=(screen_width // 2, (screen_height // 2) + 200))
    screen.blit(text, text_rect)
    screen.blit(score, text_scr)
    screen.blit(info, text_inf)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            pygame.quit()
            sys.exit()

def around_the_map(pos_x, pos_y, screen_width, screen_height):
    new_x = pos_x % screen_width
    new_y = pos_y % screen_height
    return new_x, new_y

def compare(player_placement, food_placement):
    return player_placement.colliderect(food_placement)

def collision(snake_head, snake_body):
    for segment in snake_body[1:]:
        if snake_head.colliderect(segment):
            return True
    return False

def movement(prev_dir, curr_dir, run, player, c):
    head = player[0]
    if curr_dir == "l":
        if(prev_dir == "r"):
            run = False
            game_over_screen(screen, screen_width, screen_height, c)
        else:
            new_head = pygame.Rect(head.x - 30, head.y, 30, 30)
    elif curr_dir == "r":
        if (prev_dir == "l"):
            run = False
            game_over_screen(screen, screen_width, screen_height, c)
        else:
            new_head = pygame.Rect(head.x + 30, head.y, 30, 30)
    elif curr_dir == "u":
        if (prev_dir == "d"):
            run = False
            game_over_screen(screen, screen_width, screen_height, c)
        else:
            new_head = pygame.Rect(head.x, head.y - 30, 30, 30)
    elif curr_dir == "d":
        if (prev_dir == "u"):
            run = False
            game_over_screen(screen, screen_width, screen_height, c)
        else:
            new_head = pygame.Rect(head.x, head.y + 30, 30, 30)
    else:
        return
    new_head.x, new_head.y = around_the_map(new_head.x, new_head.y, screen_width, screen_height)
    player.insert(0, new_head)
    player.pop()
    return player


black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

pygame.init()
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake')
total_time = 5 * 60 * 1000
start_time = pygame.time.get_ticks()

FPS = 10
clock = pygame.time.Clock()
box = pygame.Rect(300, 300, 30, 30)
body_list = [box]
food = pygame.Rect(random.randint(0, screen_width - 30), random.randint(0, screen_height - 30), 20, 20)
running = True
current_dir = "d"
previous_dir = "d"
counter = 0

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit(0)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        previous_dir = current_dir
        current_dir = "l"
    if keys[pygame.K_RIGHT]:
        previous_dir = current_dir
        current_dir = "r"
    if keys[pygame.K_UP]:
        previous_dir = current_dir
        current_dir = "u"
    if keys[pygame.K_DOWN]:
        previous_dir = current_dir
        current_dir = "d"

    movement(previous_dir, current_dir, running, body_list, counter)

    if compare(body_list[0], food):
        counter = counting_score(counter)
        add_snake_segment(body_list, current_dir, 30)
        food = pygame.Rect(random.randint(0, screen_width - 30), random.randint(0, screen_height - 30), 20, 20)

    screen.fill(black)
    pygame.draw.rect(screen, blue, food)
    for segment in body_list:
        pygame.draw.rect(screen, green, segment)

    if collision(body_list[0], body_list):
        running = False
        game_over_screen(screen, screen_width, screen_height, counter)

    font = pygame.font.Font(None, 100)
    text = font.render(f"Score: {counter}", True, (255, 255, 255))
    screen.blit(text, (10, 10))
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time
    remaining_time = max(0, total_time - elapsed_time)

    minutes = remaining_time // 60000
    seconds = (remaining_time % 60000) // 1000

    font = pygame.font.Font(None, 50)
    timer_text = font.render(f"{minutes:02}:{seconds:02}", True, (255, 255, 255))
    screen.blit(timer_text, (screen_width - 150, 10))

    if remaining_time <= 0:
        game_over_screen(screen, screen_width, screen_height, counter)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
