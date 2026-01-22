import pygame as pg #import pygame library

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

#Function to draw the grid
def draw_grid():
    for x in range(0, WIDTH, BLOCK_SIZE):
        pg.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT), GRID_WIDTH)
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pg.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y), GRID_WIDTH)

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
player_pos = pg.Vector2(player_grid_x * BLOCK_SIZE + BLOCK_SIZE/2, player_grid_y * BLOCK_SIZE + BLOCK_SIZE/2)
move_timer = 0

#Main Game Loop
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    screen.fill(BACKGROUND_COLOR)

    draw_grid()
    pg.draw.circle(screen, PLAYER_COLOR, player_pos, PLAYER_RADIUS) #draw the player



    move_timer += dt
    if move_timer >= MOVE_DELAY:
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            player_grid_y -= 1
            move_timer = 0
        if keys[pg.K_s]:
            player_grid_y += 1
            move_timer = 0
        if keys[pg.K_a]:
            player_grid_x -= 1
            move_timer = 0
        if keys[pg.K_d]:
            player_grid_x += 1
            move_timer = 0
        

        player_pos.x = player_grid_x * BLOCK_SIZE + BLOCK_SIZE/2
        player_pos.y = player_grid_y * BLOCK_SIZE + BLOCK_SIZE/2

        if  player_grid_x < 0:
            player_grid_x = WIDTH//BLOCK_SIZE - 1
        if player_grid_x >= WIDTH//BLOCK_SIZE:
            player_grid_x = 0
        if player_grid_y < 0:
            player_grid_y = HEIGHT//BLOCK_SIZE - 1
        if player_grid_y >= HEIGHT//BLOCK_SIZE:
            player_grid_y = 0


    #RENDER GAME HERE
    pg.display.flip()
    dt = clock.tick(FPS) / 1000 #60 FPS

pg.quit()