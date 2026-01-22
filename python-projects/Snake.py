import pygame as pg  # Import pygame library for game development
import random  # Import random for generating random food positions

# ========== GAME CONSTANTS ==========
WIDTH, HEIGHT = 1200, 700  # Window dimensions (width x height in pixels)
FPS = 60  # Frames per second - controls game loop speed
PLAYER_SPEED = 300  # Player movement speed (not currently used with grid-based movement)
PLAYER_RADIUS = 15  # Radius of player circle (not used with rectangle rendering)
PLAYER_COLOR = "black"  # Color of the snake body
BACKGROUND_COLOR = "gray"  # Background color of the game window
WINDOW_TITLE = "Snake"  # Title displayed in the window bar
BLOCK_SIZE = 30  # Size of each grid cell in pixels
GRID_COLOR = "black"  # Color of grid lines
GRID_WIDTH = 1  # Width of grid lines in pixels
MOVE_DELAY = 0.15  # Time in seconds between snake movements (controls snake speed)
PLAYER_LENGTH = 1  # Initial length of the snake (increases when food is eaten)
FOOD_RADIUS = 10  # Radius of the food circle
FOOD_COLOR = "red"  # Color of the food


# ========== HELPER FUNCTIONS ==========

def draw_grid():
    """
    Draws a grid on the screen to visualize the game grid.
    Draws vertical and horizontal lines spaced by BLOCK_SIZE.
    """
    # Draw vertical lines
    for x in range(0, WIDTH, BLOCK_SIZE):
        pg.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT), GRID_WIDTH)
    # Draw horizontal lines
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pg.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y), GRID_WIDTH)


def spawn_food():
    """
    Generates a random food position on the grid.
    Returns a Vector2 with pixel coordinates centered in a random grid cell.
    """
    # Calculate grid dimensions (number of cells)
    grid_width = WIDTH//BLOCK_SIZE
    grid_height = HEIGHT//BLOCK_SIZE
    # Generate random grid coordinates
    food_grid_x = random.randint(0, grid_width - 1)
    food_grid_y = random.randint(0, grid_height - 1)
    # Convert grid coordinates to pixel coordinates (centered in cell)
    food_pos = pg.Vector2(food_grid_x * BLOCK_SIZE + BLOCK_SIZE/2, food_grid_y * BLOCK_SIZE + BLOCK_SIZE/2)
    return food_pos

# ========== PYGAME INITIALIZATION ==========
pg.init()  # Initialize all pygame modules
screen = pg.display.set_mode((WIDTH, HEIGHT))  # Create the game window
pg.display.set_caption(WINDOW_TITLE)  # Set the window title
clock = pg.time.Clock()  # Create clock object to control frame rate
running = True  # Game loop control variable
dt = 0  # Delta time - time since last frame (in seconds)

# ========== GAME STATE INITIALIZATION ==========
# Calculate starting position (center of screen in grid coordinates)
player_grid_x = int(screen.get_width()/2/BLOCK_SIZE)
player_grid_y = int(screen.get_height()/2/BLOCK_SIZE)
# Initialize snake body as a list of grid positions (head is first element)
snake_body = [(player_grid_x, player_grid_y)]
# Convert grid position to pixel position (centered in cell)
player_pos = pg.Vector2(player_grid_x * BLOCK_SIZE + BLOCK_SIZE/2, player_grid_y * BLOCK_SIZE + BLOCK_SIZE/2)
move_timer = 0  # Timer to track time since last movement
direction = pg.Vector2(0, 0)  # Current movement direction (0,0 = not moving)
next_direction = pg.Vector2(0, 0)  # Queued direction change (prevents instant reversal)

# Spawn initial food on the board
food_pos = spawn_food()

# ========== MAIN GAME LOOP ==========
while running:
    # Handle events (window close, keyboard, etc.)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False  # Exit game loop when window is closed
    
    # Clear the screen with background color
    screen.fill(BACKGROUND_COLOR)

    # Optional: Draw grid for visual reference (currently commented out)
    # draw_grid()

    # Draw snake body - each segment is drawn as a rectangle
    for body_part in snake_body:
        # Convert grid coordinates to pixel coordinates (centered in cell)
        body_part_pos = pg.Vector2(body_part[0] * BLOCK_SIZE + BLOCK_SIZE/2, body_part[1] * BLOCK_SIZE + BLOCK_SIZE/2)
        # Alternative: Draw as circle (currently commented out)
        #pg.draw.circle(screen, PLAYER_COLOR, body_part_pos, PLAYER_RADIUS)
        # Draw each body segment as a filled rectangle
        pg.draw.rect(screen, PLAYER_COLOR, (body_part[0] * BLOCK_SIZE, body_part[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    
    # Draw food as a circle
    pg.draw.circle(screen, FOOD_COLOR, food_pos, FOOD_RADIUS)


    # ========== MOVEMENT SYSTEM ==========
    # Accumulate time since last movement
    move_timer += dt
    # Only move when enough time has passed (controls snake speed)
    if move_timer >= MOVE_DELAY:
        # Get current keyboard state
        keys = pg.key.get_pressed()
        
        # Handle direction input - prevent reversing into itself
        # W key: Move up (if not currently moving down)
        if keys[pg.K_w] and direction != pg.Vector2(0, 1):
            next_direction = pg.Vector2(0, -1)
        # S key: Move down (if not currently moving up)
        if keys[pg.K_s] and direction != pg.Vector2(0, -1):
            next_direction = pg.Vector2(0, 1)
        # A key: Move left (if not currently moving right)
        if keys[pg.K_a] and direction != pg.Vector2(1, 0):
            next_direction = pg.Vector2(-1, 0)
        # D key: Move right (if not currently moving left)
        if keys[pg.K_d] and direction != pg.Vector2(-1, 0):
            next_direction = pg.Vector2(1, 0)

        # Apply queued direction change
        if next_direction != pg.Vector2(0, 0):
            direction = next_direction
        
        # Move snake if it has a direction
        if direction != pg.Vector2(0, 0):
            # Get current head position from snake body
            player_grid_x = snake_body[0][0]
            player_grid_y = snake_body[0][1]

            # Calculate new head position by adding direction
            player_grid_x += int(direction.x)
            player_grid_y += int(direction.y)

            # Store new head position as tuple
            new_head = (player_grid_x, player_grid_y)

            # ========== COLLISION DETECTION ==========
            # Check if new head collides with body (exclude tail since it will move)
            body_to_check = snake_body[:-1] if len(snake_body) > 1 else []
            # If collision detected, end the game
            if new_head in body_to_check:
                running = False
                print("Game Over - Snake collided with itself!")
                break

            # Add new head to front of snake body
            snake_body.insert(0, new_head)

            # Remove tail if snake is longer than PLAYER_LENGTH
            if len(snake_body) > PLAYER_LENGTH:
                snake_body.pop()
        
            # Update pixel position for rendering (centered in grid cell)
            player_pos.x = player_grid_x * BLOCK_SIZE + BLOCK_SIZE/2
            player_pos.y = player_grid_y * BLOCK_SIZE + BLOCK_SIZE/2

            # Reset movement timer
            move_timer = 0

        # ========== FOOD COLLISION DETECTION ==========
        # Convert food pixel position to grid coordinates
        food_grid_x = int(food_pos.x - BLOCK_SIZE/2)/BLOCK_SIZE
        food_grid_y = int(food_pos.y - BLOCK_SIZE/2)/BLOCK_SIZE

        # Check if snake head is on the same grid cell as food
        if food_grid_x == player_grid_x and food_grid_y == player_grid_y:
            food_pos = spawn_food()  # Spawn new food at random location
            PLAYER_LENGTH += 1  # Increase snake length
        
        # ========== BOUNDARY WRAPPING ==========
        # Get current head position
        player_grid_x = snake_body[0][0]
        player_grid_y = snake_body[0][1]

        # Wrap around screen edges (teleport to opposite side)
        # Left edge: wrap to right side
        if player_grid_x < 0:
            player_grid_x = WIDTH//BLOCK_SIZE - 1
        # Right edge: wrap to left side
        if player_grid_x >= WIDTH//BLOCK_SIZE:
            player_grid_x = 0
        # Top edge: wrap to bottom
        if player_grid_y < 0:
            player_grid_y = HEIGHT//BLOCK_SIZE - 1
        # Bottom edge: wrap to top
        if player_grid_y >= HEIGHT//BLOCK_SIZE:
            player_grid_y = 0

        # Update head position if wrapping occurred
        if len(snake_body) > 0:
            snake_body[0] = (player_grid_x, player_grid_y)
            # Update pixel position for rendering
            player_pos.x = player_grid_x * BLOCK_SIZE + BLOCK_SIZE/2
            player_pos.y = player_grid_y * BLOCK_SIZE + BLOCK_SIZE/2



    # ========== RENDERING ==========
    # Update the display to show all drawn elements
    pg.display.flip()
    # Control frame rate and calculate delta time (time since last frame)
    dt = clock.tick(FPS) / 1000  # Convert milliseconds to seconds

# ========== CLEANUP ==========
# Quit pygame and clean up resources
pg.quit()