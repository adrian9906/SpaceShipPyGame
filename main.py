import random
import pygame
from actions.bullet import bulletShot
from actions.colition import isColition, isColitionShip_Enemy
from actions.gameOver import printGameOver
from actions.points import printPoint
from enemy.enemyRol import enemy_func
from pygame import mixer
from player.playerRol import player_func

pygame.init()

screen = pygame.display.set_mode((1024,600))

pygame.display.set_caption("Invasión espacial")

ico = pygame.image.load('./asset/icons8-flying-saucer-32.png')

background = pygame.image.load('./asset/fondo.jpg')

mixer.music.load('./asset/Ghostbusters.mp3')
mixer.music.play(-1)
musicShot = mixer.Sound('./asset/shot.mp3')
soundHit = mixer.Sound('./asset/hit.mp3')

x = (1024/2)-64
y = 500

x_change = 0
y_change = 0
pygame.display.set_icon(ico)

imagePlayer = pygame.image.load('./asset/icons8-launch-64.png')


x_enemy = []
y_enemy = [] 
x_change_enemy = []
y_change_enemy = []

imageEnemy = []

enemys = 20

for e in range(enemys):
    x_enemy.append(random.randint(0,(1024-64)))
    y_enemy.append(random.randint(50,200))
    x_change_enemy.append(0.7)
    y_change_enemy.append(50)
    imageEnemy.append(pygame.image.load('./asset/enemigo.png'))

points = 0

font = pygame.font.Font('freesansbold.ttf',32)

gameOverFont = pygame.font.Font('freesansbold.ttf', 80)

x_Bullet = 0
y_Bullet = 500

x_change_Bullet = 0
y_change_Bullet = 2
bulletVisible = False

imageBullet = pygame.image.load('./asset/icons8-bullet-32.png')

end = False
suma = 0
ejecute = True

while ejecute:
    screen.blit(background, (0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecute = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change-= 1
            if event.key == pygame.K_RIGHT:
                x_change+= 1
            if event.key == pygame.K_UP:
                y_change-= 1
            if event.key == pygame.K_DOWN:
                y_change+= 1
            if event.key == pygame.K_SPACE:
                musicShot.play()
                x_Bullet = x
                y_Bullet = y
                bulletVisible = bulletShot(imageBullet, screen,bulletVisible,x_Bullet,y_Bullet)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                y_change = 0
    x+= x_change
    y+=y_change
                
    if x <= 0:
        x = 0
    if x >= (1024-64):
        x=(1024-64)
    if y <= 0:
        y = 0
    if y >= 536:
        y=536
        
    for e in range(enemys):

        ## end 
        if isColitionShip_Enemy(x,x_enemy[e],y,y_enemy[e]):
            for k in range(enemys):
                y_enemy[k] = 1000
            end = True
            break
                 
        x_enemy[e]+= x_change_enemy[e]
                
        if x_enemy[e] <= 0:
            x_change_enemy[e] = 0.7
            y_enemy[e]+= y_change_enemy[e]
        if x_enemy[e] >= (1024-64):
            x_change_enemy[e]=-0.7    
            y_enemy[e]+= y_change_enemy[e]
        
        colition = isColition(x_Bullet,x_enemy[e],y_Bullet, y_enemy[e])
    
        if colition:
            soundHit.play()
            y_Bullet = 500
            x_Bullet = 0
            bulletVisible = False
            points+= 1
            x_enemy[e] = 1000
            y_enemy[e] = 1000
            suma+= x_enemy[e]
            break
            
        enemy_func(imageEnemy[e],x_enemy[e],y_enemy[e],screen)
    if suma >= enemys*1000:
        printGameOver(gameOverFont,screen)
        musicShot.stop()
        mixer.music.stop()
    
    if y_Bullet <= 64:
        y_Bullet = 500
        bulletVisible = False
        
        
        
    if bulletVisible and not end:
        bulletVisible = bulletShot(imageBullet, screen,bulletVisible,x_Bullet,y_Bullet)
        y_Bullet-= y_change_Bullet
    
    elif end:
        printGameOver(gameOverFont,screen)
        musicShot.stop()
        mixer.music.stop()
    
    player_func(imagePlayer,x,y,screen)
    
    printPoint(font, points, screen)
            
    pygame.display.update()
    
    
            
            