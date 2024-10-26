import sys
import os

try:
    import pygame
except ImportError:
    print("Pygame not found. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
    print("Pygame installed. Please restart the script.")
    sys.exit()

import pygame

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 640, 480
PLAYER_SIZE = 50
OBSTACLE_SIZE = 50
PLAYER_SPEED = 5
JUMP_HEIGHT = 20
GRAVITY = 1

# Set up some variables
player_x, player_y = WIDTH / 2, HEIGHT / 2
player_vy = 0
obstacle_x, obstacle_y = WIDTH, HEIGHT - OBSTACLE_SIZE
obstacle_speed = 5
score = 0
game_over = False
game_started = False

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_started:
                    game_started = True
                    score = 0
                    obstacle_x = WIDTH
                    obstacle_speed = 5
                    player_x, player_y = WIDTH / 2, HEIGHT / 2
                    player_vy = 0
                elif game_over:
                    game_over = False
                    score = 0
                    obstacle_x = WIDTH
                    obstacle_speed = 5
                    player_x, player_y = WIDTH / 2, HEIGHT / 2
                    player_vy = 0
                elif player_y == HEIGHT - PLAYER_SIZE:
                    player_vy = -JUMP_HEIGHT

    # Move the player
    keys = pygame.key.get_pressed()
    if game_started and not game_over:
        if keys[pygame.K_LEFT]:
            player_x -= PLAYER_SPEED
            if player_x < 0:
                player_x = 0
        if keys[pygame.K_RIGHT]:
            player_x += PLAYER_SPEED
            if player_x > WIDTH - PLAYER_SIZE:
                player_x = WIDTH - PLAYER_SIZE

        # Apply gravity
        player_y += player_vy
        player_vy += GRAVITY

        # Check for collision with the ground
        if player_y > HEIGHT - PLAYER_SIZE:
            player_y = HEIGHT - PLAYER_SIZE
            player_vy = 0

        # Move the obstacle
        obstacle_x -= obstacle_speed

        # Check for collision with the obstacle
        if (obstacle_x < player_x + PLAYER_SIZE and
                obstacle_x + OBSTACLE_SIZE > player_x and
                obstacle_y < player_y + PLAYER_SIZE and
                obstacle_y + OBSTACLE_SIZE > player_y):
            game_over = True

        # Check if the obstacle has moved off the screen
        if obstacle_x < -OBSTACLE_SIZE:
            obstacle_x = WIDTH
            score += 1
            obstacle_speed += 1

    # Draw everything
    screen.fill((0, 0, 0))
    if not game_started:
        font = pygame.font.Font(None, 36)
        text = font.render("Press Space to Start", True, (255, 255, 255))
        screen.blit(text, (WIDTH / 2 - 100, HEIGHT / 2 - 18))
    elif game_over:
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over! Press Space to Retry", True, (255, 255, 255))
        screen.blit(text, (WIDTH / 2 - 150, HEIGHT / 2 - 18))
        text = font.render(f"Final Score: {score}", True, (255, 255, 255))
        screen.blit(text, (WIDTH / 2 - 75, HEIGHT / 2 + 18))
    else:
        pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE))
        pygame.draw.rect(screen, (0, 255, 0), (obstacle_x, obstacle_y, OBSTACLE_SIZE, OBSTACLE_SIZE))
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)
