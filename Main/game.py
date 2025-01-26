import pygame
import random
from characters import PlayerShip
from math import sqrt,pow


pygame.init()

canvas = pygame.display.set_mode((1000, 667))
pygame.display.set_caption("INVASION")
icon = pygame.image.load('Icon.png')
background = pygame.image.load("backgrnd.png")
pygame.display.set_icon(icon)

# Player Details
player_image = pygame.image.load("playER.png")
ship = PlayerShip(480, 570)
player_speed = 0
player_rect = player_image.get_rect()

# Enemy Details
enemy_image = []
ufo = []
enemy_speed = []
number_of_enemies = 6
for i in range(number_of_enemies):
    load = random.randint(50, 904)
    enemy_image.append(pygame.image.load("Enemy.png"))
    ufo.append(PlayerShip(load, 0))
    enemy_speed.append(4)

# Score
score = 0
font = pygame.font.Font('Pacceti.ttf',50)
testx = 10
testy= 10

# Gameover
over_font = pygame.font.Font('Pacceti.ttf',100)


def gameovertext():
    over_value = over_font.render(f"GAME OVER", True, (255, 255, 255))
    canvas.blit(over_value, (300, 200))

def show_score(x,y):
    score_value = font.render(f"Score : {score}", True, (255,255,255))
    canvas.blit(score_value,(x,y))

# Bullet
shell = PlayerShip(ship.position_x, ship.position_y)
bullet_speed = 10
bullet_image = pygame.image.load("bullet.png")
shell_state = 'ready'
shell_rect = bullet_image.get_rect()

def iscollision(x1, x2, y1, y2):
    distance = sqrt((pow(x1 - x2, 2) + pow(y1 - y2, 2)))
    if distance < 27:
        return True
    else:
        return False


def fire_bullet():
    canvas.blit(bullet_image, (shell.position_x + 8, shell.position_y-40))
    global shell_state
    shell_state = 'Fire'


def player():
    canvas.blit(player_image, (ship.position_x, ship.position_y))


def enemy():
    for i in range(number_of_enemies):
        canvas.blit(enemy_image[i], (ufo[i].position_x, ufo[i].position_y))


running = True
while running:
    canvas.fill((140, 0, 40))
    canvas.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_speed = -5
            if event.key == pygame.K_RIGHT:
                player_speed = 5
            if event.key == pygame.K_a:
                if shell_state == "ready":
                    fire_bullet()
                    shell.position_y = ship.position_y - 4
                    shell.position_x = ship.position_x + 3

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_speed = 0

    ship.position_x += player_speed
    if ship.position_x >= 920:
        ship.position_x = 920
    elif ship.position_x <= 0:
        ship.position_x = 0
    if score < 50:
        for i in range(number_of_enemies):
            if ufo[i].position_y > 600:
                for i in range(number_of_enemies):
                    ufo[i].position_y = 2000
                gameovertext()
                break
            ufo[i].position_x += enemy_speed[i]
            if ufo[i].position_x >= 920:
                ufo[i].position_x = 920
                enemy_speed[i] = -4
                ufo[i].position_y += 80
            elif ufo[i].position_x <= 0:
                ufo[i].position_x = 0
                enemy_speed[i] = 4
                ufo[i].position_y += 30
            collision = iscollision(ufo[i].position_x, shell.position_x, ufo[i].position_y, shell.position_y)
            if collision:
                shell.position_y = ship.position_y - 4
                shell.position_x = ship.position_x + 3
                shell_state = "ready"
                score += 1
                ufo[i].position_x = random.randint(50, 904)
                ufo[i].position_y = 0
        if shell_state == 'Fire':
            fire_bullet()
            shell.position_y -= bullet_speed
        if shell.position_y <= 0:
            shell_state = 'ready'

        player()
        show_score(testx, testy)
        enemy()
    elif score > 50:
        if shell_state == 'Fire':
            fire_bullet()
            shell.position_y -= bullet_speed
        if shell.position_y <= 0:
            shell_state = 'ready'
        
    pygame.display.update()
