import pygame, sys, random
result = pygame.init()
if result[1] > 0:
    print('Ошибка инициализации Pygame : ' + str(result[1]))
    sys.exit(1)
else: 
    print('Pygame инициализирован успешно')
screen = pygame.display.set_mode((640,480))
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
bgcolor = [BLACK, GRAY, WHITE, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA]
background = BLACK
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            background = bgcolor[random.randint(0,8)]
        screen.fill(background)
        pygame.display.flip()
pygame.quit()
sys.exit(0)