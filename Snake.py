import pygame as pg #import pygame library


# Initialize Pygame
pg.init()
screen = pg.display.set_mode((1280,720)) #set the screen size
clock = pg.time.Clock() #set the clock
running = True


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    screen.fill("black")

    #RENDER GAME HERE
    pg.display.flip()
    clock.tick(60) #60 FPS

pg.quit()