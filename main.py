import pygame,random,sys
from pygame.locals import *

pygame.init()
window_size = (400,400)
clock = pygame.time.Clock()

screen = pygame.display.set_mode(window_size,0,32)
background = pygame.image.load("background.png")
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("alien.png")
pygame.display.set_icon(icon)

#kumpulan variable
playerimg = pygame.image.load("player.png").convert_alpha()
playerimg = pygame.transform.scale(playerimg,(64,64))
playerpos = [168,302]
moveright = False
moveleft = False

enemyimg = []
enemypos = [[],[]]
enemyxchange = []
enemytotal = 4

for i in range(enemytotal):
    floodfill = pygame.image.load("alien.png").convert_alpha()
    floodfill = pygame.transform.scale(floodfill,(64,64))
    enemyimg.append(floodfill)
    enemypos[0].append(random.randint(0,336))
    enemypos[1].append(random.randint(10,50))
    enemyxchange.append(3)

bulletimg = pygame.image.load('bullet.png').convert_alpha()
bulletimg = pygame.transform.scale(bulletimg,(8,16))
bulletpos = [(playerpos[0]+28),(playerpos[1])]
bulletposchange = [0,10]
bullet_state = "ready"

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 32)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (100, 125))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x,y))


def iscollision(enemyr,bulletr):
    collided = []
    value = []
    for a in range(len(enemyr)):
        if bulletr.colliderect(enemyr[a]):
            collided.append(True)
            value.append(a)
        else:
            collided.append(False)
    value.insert(0,True if any(collided) else False)
    return value


while True:
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    screen.blit(playerimg,(playerpos[0],playerpos[1]))

    bullet_rect = pygame.Rect(bulletpos[0],bulletpos[1],8,16)
    enemy_rect = []

    for i in range(enemytotal):
        enemy_rect.append(pygame.Rect(enemypos[0][i]+11,enemypos[1][i]+10,45,45))
        screen.blit(enemyimg[i],(enemypos[0][i],enemypos[1][i]))

    if moveright:
        playerpos[0] += 7
    if moveleft:
        playerpos[0] -= 7

    if playerpos[0] < 0:
        playerpos[0] = 0
    if playerpos[0] > 336:
        playerpos[0] = 336

    for i in range(enemytotal):
        if enemypos[1][i] > 340:
            for j in range(enemytotal):
                enemypos[1][j] = 2000
                game_over_text()
                break
        enemypos[0][i] += enemyxchange[i]
        if enemypos[0][i] <= 0:
            enemyxchange[i] = 3
            enemypos[1][i] += 10
        elif enemypos[0][i] >= 336:
            enemyxchange[i] = -3
            enemypos[1][i] += 10

        collision = iscollision(enemy_rect,bullet_rect)
        if collision[0] and bullet_state == "fire":
            bulletpos[1] = 302
            bullet_state = "ready"
            enemypos[0][collision[1]] = random.randint(0,336)
            enemypos[1][collision[1]] = random.randint(10,50)
            screen.blit(enemyimg[i],(enemypos[0][i],enemypos[1][i]))
            score_value += 1

    if bulletpos[1] <= 0:
        bulletpos[1] = 302
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletpos[0],bulletpos[1])
        bulletpos[1] -= bulletposchange[1]

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                moveleft = True
            if event.key == K_RIGHT:
                moveright = True
            if event.key == K_SPACE:
                if bullet_state == "ready":
                    bulletpos[0] = playerpos[0] + 28
                    bullet_rect = pygame.Rect(bulletpos[0], bulletpos[1], 8, 16)
                    fire_bullet(bulletpos[0], bulletpos[1])
        if event.type == KEYUP:
            if event.key == K_LEFT:
                moveleft = False
            if event.key == K_RIGHT:
                moveright = False
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    show_score(textX,testY)
    clock.tick(60)
    pygame.display.update()
