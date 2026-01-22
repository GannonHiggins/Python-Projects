import pygame as pg #import pygame library
import random

#Constants
WIDTH, HEIGHT = 1200, 700
FPS = 60
PLAYER_SPEED = 300
PLAYER_RADIUS = 15
PLAYER_COLOR = "black"
BACKGROUND_COLOR = "gray"
WINDOW_TITLE = "Snake"
BLOCK_SIZE = 30
GRID_COLOR = "black"
GRID_WIDTH = 1
MOVE_DELAY = 0.15 #Time between moves
PLAYER_LENGTH = 1
FOOD_RADIUS = 10
FOOD_COLOR = "red"


#Function to draw the grid
def draw_grid():
    for x in range(0, WIDTH, BLOCK_SIZE):
        pg.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT), GRID_WIDTH)
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pg.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y), GRID_WIDTH)


def spawn_food():
    grid_width = WIDTH//BLOCK_SIZE
    grid_height = HEIGHT//BLOCK_SIZE
    food_grid_x = random.randint(0, grid_width - 1)
    food_grid_y = random.randint(0, grid_height - 1)
    food_pos = pg.Vector2(food_grid_x * BLOCK_SIZE + BLOCK_SIZE/2, food_grid_y * BLOCK_SIZE + BLOCK_SIZE/2)
    return food_pos

# Initialize Pygame
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT)) #set the screen size
pg.display.set_caption(WINDOW_TITLE) #set the window title
clock = pg.time.Clock() #set the clock
running = True
dt = 0


#Player Position
player_grid_x = int(screen.get_width()/2/BLOCK_SIZE)
player_grid_y = int(screen.get_height()/2/BLOCK_SIZE)
snake_body = [(player_grid_x, player_grid_y)]
player_pos = pg.Vector2(player_grid_x * BLOCK_SIZE + BLOCK_SIZE/2, player_grid_y * BLOCK_SIZE + BLOCK_SIZE/2)
move_timer = 0
direction = pg.Vector2(0, 0)
next_direction = pg.Vector2(0, 0)

food_pos = spawn_food()

#Main Game Loop
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    screen.fill(BACKGROUND_COLOR)

    draw_grid()

    for body_part in snake_body:
        body_part_pos = pg.Vector2(body_part[0] * BLOCK_SIZE + BLOCK_SIZE/2, body_part[1] * BLOCK_SIZE + BLOCK_SIZE/2)
        pg.draw.circle(screen, PLAYER_COLOR, body_part_pos, PLAYER_RADIUS)
    
    pg.draw.circle(screen, FOOD_COLOR, food_pos, FOOD_RADIUS) #draw the food


    move_timer += dt
    if move_timer >= MOVE_DELAY:
        keys = pg.key.get_pressed()
        if keys[pg.K_w] and direction != pg.Vector2(0, 1):
            next_direction = pg.Vector2(0, -1)
        if keys[pg.K_s] and direction != pg.Vector2(0, -1):
            next_direction = pg.Vector2(0, 1)
        if keys[pg.K_a] and direction != pg.Vector2(1, 0):
            next_direction = pg.Vector2(-1, 0)
        if keys[pg.K_d] and direction != pg.Vector2(-1, 0):
            next_direction = pg.Vector2(1, 0)

        if next_direction != pg.Vector2(0, 0):
            direction = next_direction
        
        if direction != pg.Vector2(0, 0):
            player_grid_x = snake_body[0][0]
            player_grid_y = snake_body[0][1]

            player_grid_x += int(direction.x)
            player_grid_y += int(direction.y)

            snake_body.insert(0, (player_grid_x, player_grid_y))

            if len(snake_body) > PLAYER_LENGTH:
                snake_body.pop()
        

            player_pos.x = player_grid_x * BLOCK_SIZE + BLOCK_SIZE/2
            player_pos.y = player_grid_y * BLOCK_SIZE + BLOCK_SIZE/2

            move_timer = 0

        food_grid_x = int(food_pos.x - BLOCK_SIZE/2)/BLOCK_SIZE
        food_grid_y = int(food_pos.y - BLOCK_SIZE/2)/BLOCK_SIZE

        if food_grid_x == player_grid_x and food_grid_y == player_grid_y:
            food_pos = spawn_food()
            PLAYER_LENGTH += 1

        player_grid_x = snake_body[0][0]
        player_grid_y = snake_body[0][1]

        if  player_grid_x < 0:
            player_grid_x = WIDTH//BLOCK_SIZE - 1
        if player_grid_x >= WIDTH//BLOCK_SIZE:
            player_grid_x = 0
        if player_grid_y < 0:
            player_grid_y = HEIGHT//BLOCK_SIZE - 1
        if player_grid_y >= HEIGHT//BLOCK_SIZE:
            player_grid_y = 0

        if len(snake_body) > 0:
            snake_body[0] = (player_grid_x, player_grid_y)
            player_pos.x = player_grid_x * BLOCK_SIZE + BLOCK_SIZE/2
            player_pos.y = player_grid_y * BLOCK_SIZE + BLOCK_SIZE/2


    #RENDER GAME HERE
    pg.display.flip()
    dt = clock.tick(FPS) / 1000 #60 FPS

pg.quit()