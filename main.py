import pygame
from sys import exit
from random import randint

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Dinosaur Runner')
clock = pygame.time.Clock()
font = pygame.font.Font('graphics/Pixeltype.ttf', 35)
game_active = False
start_time = 0
score = 0

# Background
sky_surface = pygame.image.load('graphics/sky.png').convert_alpha()
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()

# Obstacle
fireball_surface = pygame.image.load('graphics/fireball.png').convert_alpha()

obstacle_rect_list = []

# Player
player_surface = pygame.image.load('graphics/player.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom=(100, 500))
player_gravity = 0

# intro screen
player_stand = pygame.image.load('graphics/player.png').convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
player_stand_rect = player_stand.get_rect(center=(400, 300))

game_title = font.render('Dino jump', False, 'black')
game_title_rect = game_title.get_rect(center=(400, 100))

game_message = font.render('press space to run', False, 'black')
game_message_rect = game_message.get_rect(center=(400, 500))

# Obstacle timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1600)


def display_score():
    current_score = (pygame.time.get_ticks() // 100) - start_time
    scoreboard_surface = font.render(f'Score: {current_score}', False, 'black')
    scoreboard_rect = scoreboard_surface.get_rect(center=(100, 30))
    screen.blit(scoreboard_surface, scoreboard_rect)
    return current_score


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            screen.blit(fireball_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []


def collision(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if obstacle_rect.colliderect(player):
                return False
    return True


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom == 500:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -20
                    player_rect.y += player_gravity
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 500:
                    player_gravity = -20
                    player_rect.y += player_gravity
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(fireball_surface.get_rect(bottomright=(randint(900, 1100), 500)))
                else:
                    obstacle_rect_list.append(fireball_surface.get_rect(bottomright=(randint(900, 1100), 400)))
        # Restart game
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = (pygame.time.get_ticks() // 100)

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 500))
        # pygame.draw.rect(screen, 'darkseagreen1', score_rect)
        # pygame.draw.rect(screen, 'darkseagreen1', score_rect, 10)
        # screen.blit(score_surface, score_rect)
        score = display_score()

        # fireball_rect.x -= 5
        # if fireball_rect.right < 0: fireball_rect.left = 800
        # screen.blit(fireball_surface, fireball_rect)

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 500:
            player_rect.bottom = 500
        screen.blit(player_surface, player_rect)

        # Obstacle control
        obstacle = obstacle_movement(obstacle_rect_list)

        # Collusion
        game_active = collision(player_rect, obstacle_rect_list)

    # Death screen
    else:
        screen.fill('darkseagreen2')
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_title, game_title_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (100, 500)
        player_gravity = 0

        if score > 0:
            score_message = font.render(f'{score}', False, 'black')
            score_rect = score_message.get_rect(center=(400, 500))
            screen.blit(score_message, score_rect)
        else:
            screen.blit(game_message, game_message_rect)

    pygame.display.update()
    fps = clock.tick(60)

