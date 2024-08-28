import pygame, sys
from pygame.locals import *

size = 720, 480
width, height = size
result = pygame.init()
if result[1] > 0:
    print('Ошибка инициализации Pygame : ' + str(result[1]))
    sys.exit(1)
else: 
    print('Pygame инициализирован успешно')
screen = pygame.display.set_mode((size))
BLUE = (150,150,255)
RED = (255,0,0)
ball = pygame.image.load('ball_transparent.gif')
rect = ball.get_rect()
speed = [2,2]

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    rect = rect.move(speed)
    if rect.left < 0 or rect.right > width:
        speed[0] = -speed[0]
    if rect.top < 0 or rect.bottom > height:
        speed[1] = -speed[1]
    
    screen.fill(BLUE)
    screen.blit(ball, rect)
    pygame.time.Clock().tick(240)
    pygame.display.flip()

pygame.quit()
sys.exit(0)