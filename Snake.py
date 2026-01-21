import pygame as pg #import pygame library


WIDTH, HEIGHT = 1280, 720
FPS = 60
PLAYER_SPEED = 300
PLAYER_RADIUS = 15
PLAYER_COLOR = "black"
BACKGROUND_COLOR = "gray"
WINDOW_TITLE = "Snake"
BLOCK_SIZE = 30
GRID_COLOR = "black"
GRID_WIDTH = 1

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

player_pos = pg.Vector2(screen.get_width()/2, screen.get_height()/2) #set the player position to the center of the screen

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    screen.fill(BACKGROUND_COLOR)
    draw_grid()
    pg.draw.circle(screen, PLAYER_COLOR, player_pos, PLAYER_RADIUS) #draw the player

    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        player_pos.y -= PLAYER_SPEED * dt
    if keys[pg.K_s]:
        player_pos.y += PLAYER_SPEED * dt
    if keys[pg.K_a]:
        player_pos.x -= PLAYER_SPEED * dt
    if keys[pg.K_d]:
        player_pos.x += PLAYER_SPEED * dt

    #RENDER GAME HERE
    pg.display.flip()
    dt = clock.tick(FPS) / 1000 #60 FPS

pg.quit()