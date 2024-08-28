import pygame, sys
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
colors = [WHITE, RED, BLUE, GREEN]

size = 720, 480
width, height = size
BALL_SIZE = 25

class Ball:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0
        self.color = colors[random.randint(0,3)]

def make_ball():
        ball = Ball()
        ball.x = random.randrange(BALL_SIZE, width - BALL_SIZE)
        ball.y = random.randrange(BALL_SIZE, height - BALL_SIZE)
        ball.change_x = random.randint(1,3)
        ball.change_y = random.randint(1,3)
        return ball
    

result = pygame.init()
if result[1] > 0:
    print('Ошибка инициализации Pygame : ' + str(result[1]))
    sys.exit(1)
else: 
    print('Pygame инициализирован успешно')
screen = pygame.display.set_mode((size))
pygame.display.set_caption("Bouncing Balls")

fps = 30
ball_list = []
ball = make_ball()
ball_list.append(ball)

running = False
while not running:
     for event in pygame.event.get():
        if event.type ==  pygame.QUIT:
               running = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if len(ball_list) < 5:
                      ball = make_ball()
                      ball_list.append(ball)
                else:
                     print("На экране слишком много мячей")
            elif event.key == pygame.K_BACKSPACE:
                 if len(ball_list) == 0:
                      print('Мячей нет')
                 else:
                      ball_list.pop()
            elif event.key == pygame.K_q:
                 if fps == 30:
                      print("Минимальная скорость обновления кадров")
                 else:
                    fps = fps - 30
                    print('Текущий ФПС : ' + str(fps)) 
            elif event.key == pygame.K_e:
                 if fps == 300:
                       print("Максимальная скорость обновления кадров")     
                 else:
                      fps = fps + 30
                      print('Текущий ФПС : ' + str(fps)) 
            elif event.key == pygame.K_r:
                for ball in ball_list:
                     ball.change_x = random.randint(-2,3)
                     ball.change_y = random.randint(-2,3)
                     ball.color = colors[random.randint(0,3)]

     for ball in ball_list:
        ball.x = ball.x + ball.change_x
        ball.y = ball.y + ball.change_y

        if ball.y > height - BALL_SIZE or ball.y < BALL_SIZE:
            ball.change_y = -ball.change_y
        if ball.x > width - BALL_SIZE or ball.x < BALL_SIZE:
            ball.change_x = -ball.change_x

     screen.fill(BLACK)
     for ball in ball_list:
        pygame.draw.circle(screen, ball.color, [ball.x, ball.y], BALL_SIZE)

     pygame.time.Clock().tick(fps)
     pygame.display.flip()

pygame.quit()
sys,exit(0)