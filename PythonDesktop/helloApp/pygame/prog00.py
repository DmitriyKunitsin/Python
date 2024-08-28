import pygame, sys
result = pygame.init()
if result[1] > 0:
    print('Ошибка инициализации Pygame : ' + str(result[1]))

    sys.exit(1)
else:
    print('Pygame инициализирован успешно')
screen = pygame.display.set_mode((640,480))
pygame.quit()
sys.exit(0)