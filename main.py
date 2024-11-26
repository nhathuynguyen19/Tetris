import pygame, random, os
from modules import Tetrimino
from config.constants import *
from modules.utils import downcolor
from modules import GameGrid

pygame.init()

# path
font_home_video = os.path.join(os.getcwd(), 'assets', 'fonts', 'HomeVideo-BLG6G.ttf')
font_home_video_bold = os.path.join(os.getcwd(), 'assets', 'fonts', 'HomeVideoBold-R90Dv.ttf')
best_score_path = os.path.join(os.getcwd(), 'assets', 'data', 'best_score.txt')
logo_path = os.path.join(os.getcwd(), 'assets', 'images', 'logo.ico')

# font
font1 = pygame.font.Font(font_home_video, 12)
font2 = pygame.font.Font(font_home_video_bold, 30)
            
def draw_tetrimino(tetrimino):
    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
                if cell == 1 and not tetrimino.check_collision(game_grid.grid): 
                    color_down = downcolor(tetrimino.color)
                    pygame.draw.rect(screen, tetrimino.color, ((tetrimino.x + x) * BLOCK_SIZE, (tetrimino.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(screen, color_down, ((tetrimino.x + x) * BLOCK_SIZE, (tetrimino.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_tetrimino_game_table(tetrimino):
    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
            if cell == 1:
                color_down = downcolor(tetrimino.color)
                pygame.draw.rect(screen, tetrimino.color, ((COLUMNS + x + 3 - len(row)/2) * BLOCK_SIZE, ((3 + y - len(tetrimino.shape)/2) * BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, color_down, ((COLUMNS + x + 3 - len(row)/2) * BLOCK_SIZE, ((3 + y - len(tetrimino.shape)/2) * BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE), 1)

screen = pygame.display.set_mode((GAME_WIDTH + BLOCK_SIZE * 6, GAME_HEIGHT))
pygame.display.set_caption("Tetris")
icon_logo = pygame.image.load(logo_path)
pygame.display.set_icon(icon_logo)
clock = pygame.time.Clock()
running = True
game_grid = GameGrid(ROWS, COLUMNS)
tetrimino_bag = [0, 1, 2, 3, 4, 5, 6]
current_position_tetrimino = random.choice(tetrimino_bag)

tetrimino = Tetrimino(SHAPES[current_position_tetrimino], COLORS[current_position_tetrimino])
random_rotate = random.choice([0, 1, 2, 3])
for i in range(random_rotate):
    tetrimino.rotate()
tetrimino.set_y(tetrimino.default_y())
after_tetrimino = tetrimino

position_after_tetrimino = current_position_tetrimino

game_time = 0
move_delay = 40
last_move_time = 0
is_pressed = False
top_grid = 0
score = 0
score_to_level_up = 100
level_game = 1
lines_delete = 0
table_draw = True
get_after_tetrimino = False
is_place_tetrimino = False
game_over = False
begin_game = True
best_score = 0

# score file data
if not os.path.exists(best_score_path):
    with open(best_score_path, 'w') as file:
        file.write("0")
with open(best_score_path, 'r') as file:
    best_score = int(file.read())  

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                tetrimino.rotate()
                if tetrimino.check_collision(game_grid.grid):
                    for i in range(3):
                        tetrimino.rotate()
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                tetrimino.y += 1
                is_pressed = True
                if tetrimino.check_collision(game_grid.grid):
                    tetrimino.y -= 1
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                tetrimino.x -= 1
                is_pressed = True
                if tetrimino.check_collision(game_grid.grid):
                    tetrimino.x += 1
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                tetrimino.x += 1
                is_pressed = True
                if tetrimino.check_collision(game_grid.grid):
                    tetrimino.x -= 1
    
    
    current_time = pygame.time.get_ticks()
    if current_time - last_move_time > move_delay and not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            tetrimino.y += 1
            if is_pressed:
                tetrimino.y -= 1
                is_pressed = False
            if tetrimino.check_collision(game_grid.grid):
                tetrimino.y -= 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            tetrimino.x -= 1
            if is_pressed:
                tetrimino.x += 1
                is_pressed = False
            if tetrimino.check_collision(game_grid.grid):
                tetrimino.x += 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            tetrimino.x += 1
            if is_pressed:
                tetrimino.x -= 1
                is_pressed = False
            if tetrimino.check_collision(game_grid.grid):
                tetrimino.x -= 1
        
        last_move_time = current_time
          
    
    # print(f"x: {tetrimino.x}, y: {tetrimino.y}")
    #level game
    if score % score_to_level_up == 0 and level_game < 10 and lines_delete >= 10:
        level_game += 1
        lines_delete = 0
    # print(f"level: {level_game}, score: {score}, lines_delete: {lines_delete}")
    text_score = font1.render(f"Score: {score}", True, WHITE)
    text_level = font1.render(f"Level: {level_game}", True, WHITE)
    text_best_score = font1.render("Best Score:", True, WHITE)
    text_best_score_number = font1.render(f"{best_score}", True, WHITE)
    
    if tetrimino_bag and position_after_tetrimino in tetrimino_bag:
        tetrimino_bag.remove(position_after_tetrimino)
    elif not tetrimino_bag:
        tetrimino_bag = list(range(7))
        random.shuffle(tetrimino_bag)
        
    # print(tetrimino_bag)
    
    if begin_game:
        temp_after_tetrimino = after_tetrimino
        position_after_tetrimino = random.choice(tetrimino_bag)
    
    table_game = pygame.Rect(COLUMNS * BLOCK_SIZE, 0, 6 * BLOCK_SIZE, ROWS * BLOCK_SIZE)
    screen.fill((20, 20, 20), table_game)
    pygame.draw.rect(screen, WHITE, (COLUMNS * BLOCK_SIZE, 0, 6 * BLOCK_SIZE, ROWS * BLOCK_SIZE), 2)
        
    if begin_game:
        tetrimino_display_table_after = temp_after_tetrimino
    else:
        tetrimino_display_table_after = Tetrimino(SHAPES[position_after_tetrimino], COLORS[position_after_tetrimino])
        
    tetrimino_display_table_after.x = 11
    tetrimino_display_table_after.y = 1
    for i in range(random_rotate):
        tetrimino_display_table_after.rotate()
    draw_tetrimino_game_table(tetrimino_display_table_after)
    screen.blit(text_score, (COLUMNS * BLOCK_SIZE + 20, 7 * BLOCK_SIZE))
    screen.blit(text_level, (COLUMNS * BLOCK_SIZE + 20, 8 * BLOCK_SIZE))
    screen.blit(text_best_score, (COLUMNS * BLOCK_SIZE + 20, 10 * BLOCK_SIZE))
    screen.blit(text_best_score_number, (COLUMNS * BLOCK_SIZE + 20, 11 * BLOCK_SIZE))
    # print(position_after_tetrimino + 1)
    
    # each frame
    if game_time % (22 - level_game*2) == 0:
        
        # update high score
        if score > best_score:
            best_score = score
            with open(best_score_path, "w") as file:
                file.write(str(best_score))
        
        if not game_over:
            tetrimino.y += 1
            if tetrimino.check_collision(game_grid.grid) and not game_over:
                tetrimino.y -= 1
                
                # update grid
                if is_place_tetrimino:
                    tetrimino.place_tetrimino(game_grid.grid)
                    
                # update grid condition
                is_place_tetrimino = True
                
                # current tetrimino
                if begin_game:
                    tetrimino = temp_after_tetrimino
                    begin_game = False
                else:
                    tetrimino = after_tetrimino
                    
                # after tetrimino
                if not begin_game:
                    position_after_tetrimino = random.choice(tetrimino_bag)
                after_tetrimino = Tetrimino(SHAPES[position_after_tetrimino], COLORS[position_after_tetrimino])
                random_rotate = random.choice([0, 1, 2, 3])
                for i in range(random_rotate):
                    after_tetrimino.rotate()
                after_tetrimino.set_y(after_tetrimino.default_y())
                
                
    # delete line
    game_grid.delete_lines(score, level_game, lines_delete)
                
    # check game over
    if top_grid >= ROWS:
        game_over = True
        is_place_tetrimino = False

    #draw game scene
    top_grid = game_grid.draw_grid(screen)
    if not game_over:
        draw_tetrimino(tetrimino)
    
    # after overgame
    if game_over:
        game_over_text = font2.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (BLOCK_SIZE * COLUMNS // 2 - game_over_text.get_width() // 2, BLOCK_SIZE * ROWS // 2 - game_over_text.get_height() // 2))
    
    # end frame
    pygame.display.flip()
    pygame.draw.rect(screen, BLACK, (0, 0, COLUMNS * BLOCK_SIZE, ROWS * BLOCK_SIZE))
    game_time += 1
    clock.tick(60)
    
pygame.quit()