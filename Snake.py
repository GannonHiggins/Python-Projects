import pygame as pg #import pygame library


# Initialize Pygame
pg.init()
screen = pg.display.set_mode((1280,720)) #set the screen size
clock = pg.time.Clock() #set the clock
running = True
dt = 0

player_pos = pg.Vector2(screen.get_width()/2, screen.get_height()/2) #set the player position to the center of the screen

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    screen.fill("black")
    pg.draw.circle(screen, "white", player_pos, 15)

    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        player_pos.y -= 300 * dt
    if keys[pg.K_s]:
        player_pos.y += 300 * dt
    if keys[pg.K_a]:
        player_pos.x -= 300 * dt
    if keys[pg.K_d]:
        player_pos.x += 300 * dt

    #RENDER GAME HERE
    pg.display.flip()
    dt = clock.tick(60) / 1000 #60 FPS

pg.quit()