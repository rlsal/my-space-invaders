import random
import math
import pygame
from pygame import mixer

# Constants
BG = 'images/background.png'
BGM = 'sound/background.wav'
LASER = 'sound/laser.wav'
EXPLOSION = 'sound/explosion.wav'
BULLET = 'images/bullet.png'
ICON = 'images/ufo.png'
PLAYER = 'images/player.png'
ENEMY_1 = 'images/alien.png'
ENEMY_2 = 'images/shipalien.png'
FONT = 'freesansbold.ttf'
STATUS_READY = 'ready'
STATUS_FIRE = 'fire'
WIDTH = 800
HEIGHT = 600
MOVEMENT_SIZE = 5
ENEMY_MOVEMENT = 4
INIT_PLAYER_X_SIZE = 370
INIT_PLAYER_Y_SIZE = 480
SPACESHIP_X_SIZE = 64
ENEMY_UPPER_START = 50
ENEMY_LOWER_START = 150
NUM_OF_ENEMIES = 6
GAME_OVER_HEIGHT = 440

# Initialize pygame
pygame.init()

# Create screen with height/width
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Background
background = pygame.image.load(BG)

# Background sound
mixer.music.load(BGM)
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(ICON)
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load(PLAYER)
player_x = INIT_PLAYER_X_SIZE
player_y = INIT_PLAYER_Y_SIZE
player_x_change = 0

# Enemies
enemy_img, enemy_x, enemy_y, enemy_x_change, enemy_y_change = [], [], [], [], []

for i in range(NUM_OF_ENEMIES):
    enemy_img.append(pygame.image.load(random.choice([ENEMY_1, ENEMY_2])))
    enemy_x.append(random.randint(0, WIDTH - SPACESHIP_X_SIZE))
    enemy_y.append(random.randint(ENEMY_UPPER_START, ENEMY_LOWER_START))
    enemy_x_change.append(ENEMY_MOVEMENT)
    enemy_y_change.append(40)

# Bullet
bullet_img = pygame.image.load(BULLET)
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
# Bullet state - ready (cant see bullet), fire(bullet moving)
bullet_state = STATUS_READY

# Score
score_value = 0
font = pygame.font.Font(FONT, 32)
text_x = 10
text_y = 10

# Game over text
over_font = pygame.font.Font(FONT, 64)
# Game over flag
is_game_over = False


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_texts():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    try_again_text = font.render("Play Again?", True, (255, 255, 255))
    #pygame.draw.rect(screen,  (0, 0, 100), [300, 80, 205, 70], 1)
    screen.blit(try_again_text, (310, 100))
    global is_game_over
    is_game_over = True


# Draw Player
def player(x, y):
    screen.blit(player_img, (x, y))


# Draw Enemy
def enemy(x, y, j):
    screen.blit(enemy_img[j], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_img, (x + 16, y + 10))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
    return True if distance < 27 else False


# Flag for running process
running = True

# Game loop
while running:
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Listen to key pressed event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change -= MOVEMENT_SIZE
            if event.key == pygame.K_RIGHT:
                player_x_change += MOVEMENT_SIZE
            if event.key == pygame.K_SPACE:
                if bullet_state == STATUS_READY:
                    bullet_sound = mixer.Sound(LASER)
                    bullet_sound.play()
                    # store static x for bullet x location travel
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            if is_game_over:
                if 500 > pygame.mouse.get_pos()[0] > 300 and 150 > pygame.mouse.get_pos()[1] > 83:
                    for i in range(NUM_OF_ENEMIES):
                        enemy_x[i] = random.randint(0, WIDTH - SPACESHIP_X_SIZE)
                        enemy_y[i] = random.randint(ENEMY_UPPER_START, ENEMY_LOWER_START)
                        score_value = 0
                is_game_over = False

    player_x += player_x_change

    # Player boundaries
    if player_x <= 0:
        player_x = 0

    right_boundary = WIDTH - SPACESHIP_X_SIZE
    if player_x >= right_boundary:
        player_x = right_boundary

    # Enemy boundaries
    for i in range(NUM_OF_ENEMIES):
        # Game over
        if enemy_y[i] > GAME_OVER_HEIGHT:
            for j in range(NUM_OF_ENEMIES):
                enemy_y[j] = 9999

            game_over_texts()
            break

        enemy_x[i] += enemy_x_change[i]

        if enemy_x[i] <= 0:
            enemy_x_change[i] = ENEMY_MOVEMENT
            enemy_y[i] += enemy_y_change[i]

        right_boundary = WIDTH - SPACESHIP_X_SIZE
        if enemy_x[i] >= right_boundary:
            enemy_x_change[i] = -ENEMY_MOVEMENT
            enemy_y[i] += enemy_y_change[i]

        # Collision
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)

        if collision:
            explosion_sound = mixer.Sound(EXPLOSION)
            explosion_sound.play()
            bullet_y = INIT_PLAYER_Y_SIZE
            bullet_state = STATUS_READY
            score_value += 1
            enemy_x[i] = random.randint(0, WIDTH - SPACESHIP_X_SIZE)
            enemy_y[i] = random.randint(ENEMY_UPPER_START, ENEMY_LOWER_START)

        enemy(enemy_x[i], enemy_y[i], i)

    # Bullet movement
    if bullet_y <= 0:
        bullet_y = INIT_PLAYER_Y_SIZE
        bullet_state = STATUS_READY

    if bullet_state == STATUS_FIRE:
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()


