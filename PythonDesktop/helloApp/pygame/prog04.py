import pygame, math, random
import time,sys

width, height = 800, 800
result = pygame.init()
if result[1] > 0:
    print('Ошибка инициализации Pygame : ' + str(result[1]))
    sys.exit(1)
else: 
    print('Pygame инициализирован успешно')
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fibonacci Tree")
screen = pygame.display.get_surface()
shift = 20
A_x = 0 + shift
A_y = 649 + shift
B_x = 750 + shift
B_y = 649 + shift
C_x = 375 + shift
C_y = 0 + shift
RGB = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]

def draw_triangle(A_x, A_y, B_x, B_y, C_x, C_y, i):
    pygame.draw.line(screen, RGB[i%3], (A_x, A_y), (B_x, B_y), 1)
    pygame.draw.line(screen, RGB[i%3], (C_x, C_y), (B_x, B_y), 1)
    pygame.draw.line(screen, RGB[i%3], (A_x, A_y), (C_x, C_y), 1)
    pygame.display.flip()

def draw_fractal(A_x, A_y, B_x, B_y, C_x, C_y, depth):
    if depth > 0:
        draw_fractal((A_x), (A_y), (A_x+B_x)/2, (A_y+B_y)/2,
        (A_x+C_x)/2, (A_y+C_y)/2, depth-1)
        draw_fractal((B_x), (B_y), (A_x+B_x)/2, (A_y+B_y)/2,
        (B_x+C_x)/2, (B_y+C_y)/2, depth-1)
        draw_fractal((C_x), (C_y), (C_x+B_x)/2, (C_y+B_y)/2,
        (A_x+C_x)/2, (A_y+C_y)/2, depth-1)
        
        draw_triangle((A_x), (A_y), (A_x+B_x)/2,
        (A_y+B_y)/2, (A_x+C_x)/2, (A_y+C_y)/2, depth)
        draw_triangle((B_x), (B_y), (A_x+B_x)/2,
        (A_y+B_y)/2, (B_x+C_x)/2, (B_y+C_y)/2, depth)
        draw_triangle((C_x), (C_y), (C_x+B_x)/2,
        (C_y+B_y)/2, (A_x+C_x)/2, (A_y+C_y)/2, depth)
    
draw_fractal(A_x, A_y, B_x, B_y, C_x, C_y, 8)
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit
sys.exit(0)

