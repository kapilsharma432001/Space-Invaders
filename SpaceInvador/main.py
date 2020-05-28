import pygame
import random
import math
from pygame import mixer

# Initialising pygame otherwise it will not work
pygame.init()
# Creating screen of pygame
screen = pygame.display.set_mode((800, 600))

# background image
bgImg = pygame.image.load("background.png")

# Background Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and Icon

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Player

playerImg = pygame.image.load("players.png")
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet

bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 40
bullet_state = "ready"  # If the state is fire than it means that bullet is currently moving and ready state means that you can't srr the bullet

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
font2 = pygame.font.Font("freesansbold.ttf", 15)
textX = 10
textY = 10
instX = 10;
instY = 50

# Game Over Text Font
over_font = pygame.font.Font("freesansbold.ttf", 100)


def game_over_text():
    game_over = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over, (80, 280))


def show_instructions(x, y):
    shoot = font2.render("Shoot using S button.", True, (255, 255, 255))
    screen.blit(shoot, (x, y))


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))  # Blit actually means to draw


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  # Blit actually means to draw


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    screen.fill((0, 0, 0))  # It should be above all otherwise all other things will be screen underneath
    # Background Image
    screen.blit(bgImg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -8
            if event.key == pygame.K_RIGHT:
                playerX_change = 8

            if event.key == pygame.K_s:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Player movemrnt
    playerX += playerX_change
    if (playerX <= 0):
        playerX = 736
    elif (playerX >= 736):
        playerX = 0

    # Enemy movement

    for i in range(num_of_enemies):
        # Game Over
        if (enemyY[i] > 440):
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if (enemyX[i] <= 0):
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif (enemyX[i] >= 736):
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    show_instructions(instX, instY)
    pygame.display.update()  # This update and display should always be in this code
