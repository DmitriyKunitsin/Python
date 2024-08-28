import pygame, sys, time, random

difficutly = 5

window_size_x = 720
window_size_y = 480
size = window_size_x, window_size_y
result = pygame.init()
if result[1] > 0:
    print('Ошибка инициализации Pygame : ' + str(result[1]))
    sys.exit(1)
else: 
    print('Pygame инициализирован успешно')
pygame.display.set_caption('Snake')
game_window = pygame.display.set_mode((size))
black = pygame.Color(0,0,0)
white = pygame.Color(255,255,255)
green = pygame.Color(0,255,0)

snake_pos = [100, 100]
snake_body = [[100,100],[100-10, 100]]
direction = 'DOWN'
change_to = direction

food_pos = [random.randrange(1, (window_size_x//10)) * 10, random.randrange(1, (window_size_y//10)) * 10]
food_spawn = True

score = 0
difficulty_counter = 0
difficulty = 5

def show_score(choice, color, font,size):
    score_font = pygame.font.SysFont(font,size)
    score_surface = score_font.render("Score : " + str(score) + ' Difficulty : ' + str(difficulty), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (window_size_x/10 + 30, 15)
    else:
        score_rect.midtop = (window_size_x/2, window_size_y/1.25)
    game_window.blit(score_surface,score_rect)

def game_over():
    game_over_font = pygame.font.SysFont('Times New Roman', 90)
    game_over_surface = game_over_font.render('Game Over', True, green)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_size_x / 2, window_size_y / 4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, green, 'Times New Roman', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit
    sys.exit(0)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    snake_body.insert(0, list(snake_pos))

    if snake_pos[0] == food_pos[0] and  snake_pos[1] == food_pos[1]:
        score = score + 1
        difficulty_counter = difficulty_counter + 1
        print(difficulty_counter)
        if difficulty_counter == 10:
            difficulty_counter = 0
            difficulty = difficulty + 5

        food_spawn = False
    else:
        snake_body.pop()
    
    if not food_spawn:
        food_pos = [random.randrange(1, (window_size_x//10)) * 10, random.randrange(1 , (window_size_y//10)) * 10]
    
    food_spawn = True

    game_window.fill(black)
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    if snake_pos[0] < 0 or snake_pos[0] > window_size_x - 10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > window_size_y - 10:
        game_over()

    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    show_score(1, white, 'Times New Roman', 20)
    pygame.display.update()
    pygame.time.Clock().tick(difficulty)