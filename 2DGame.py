import pygame
import random


# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Avoid the Falling Objects")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the clock for controlling frame rate
clock = pygame.time.Clock()

# Player settings
player_width = 50
player_height = 50
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - player_height - 10
player_speed = 7

# Add falling object settings
object_width = 50
object_height = 50
object_speed = 5
object_count = 5    # Number of falling objects
objects = []

for _ in range(object_count):
    object_x = random.randint(0, SCREEN_WIDTH - object_width)
    object_y = random.randint(-600, 0)
    objects.append([object_x, object_y])

# Score
score = 0


# Function to draw the player
def draw_player():
    pygame.draw.rect(screen, BLACK, [player_x, player_y, player_width, player_height])


# Function to draw objects
def draw_object():
    for obj in objects:
        pygame.draw.rect(screen, BLACK, [obj[0], obj[1], object_width, object_height])


def draw_score():
    font = pygame.font.SysFont(None, 35)
    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, [10, 10])


# Function for collision detection
def check_collision(player_x, player_y, object_x, object_y):
    if (object_x < player_x + player_width and object_x + object_width > player_x and
            object_y < player_y + player_height and object_y + object_height > player_y):
        return True
    return False


# Initialize Pygame mixer for sound
# pygame.mixer.init()

# Load sound effects
# move_sound = pygame.mixer.Sound('move.wav')
# collision_sound = pygame.mixer.Sound('collision.wav')
# game_over_sound = pygame.mixer.Sound('game_over.wav')


# Game state
game_over = False


# Function for restarting the game
def restart_game():
    global player_x, player_y, score, game_over, objects
    player_x = SCREEN_WIDTH // 2 - player_width // 2
    player_y = SCREEN_HEIGHT - player_height - 10
    score = 0
    game_over = False
    objects = []
    for _ in range(object_count):
        object_x = random.randint(0, SCREEN_WIDTH - object_width)
        object_y = random.randint(-600, 0)
        objects.append([object_x, object_y])


# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:     # Press 'R' to restart
                restart_game()

    if not game_over:
        # Get keys pressed and play sound
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
            # move_sound.play()
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
            player_x += player_speed
            # move_sound.play()

        # Update falling objects position
        for obj in objects:
            obj[1] += object_speed
            if obj[1] > SCREEN_HEIGHT:
                obj[1] = -object_height
                obj[0] = random.randint(0, SCREEN_WIDTH - object_width)
                score += 1  # Increment score when avoiding an object

            # Check for collision
            if check_collision(player_x, player_y, obj[0], obj[1]):
                # pygame.mixer.Sound.play(collision_sound)
                # pygame.mixer.Sound.play(game_over_sound)
                game_over = True

    # Fill the screen with a background color
    screen.fill(WHITE)

    # Draw the player and the falling objects
    if not game_over:
        draw_player()
        draw_object()
        draw_score()
    else:
        # Display "Game Over" message
        font = pygame.font.SysFont(None, 55)
        game_over_text = font.render("Game Over", True, BLACK)
        screen.blit(game_over_text, [SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2])

    # Update the display
    pygame.display.flip()

    # Limit the frame rate to 60 FPS
    clock.tick(60)

# Quit Pygame
pygame.quit()
