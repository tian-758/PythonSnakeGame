# Import libraries
import pygame
import time
from enum import Enum
import pygame.display
from snake_functions import newFruitSpawnLocation

player_speed = 15

# Window size
window_x = 720
window_y = 480

# Colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Initialize pygame
pygame.init()

# Initialize game window
pygame.display.set_caption('Snake Game')
game_window = pygame.display.set_mode((window_x, window_y))

fps = pygame.time.Clock()

snake_pos = [100, 50]

snake_body = [[100,50],[90,50],[80,50],[70,50]]

fruit_pos = newFruitSpawnLocation(window_x, window_y, snake_body)

fruit_spawn = True

class Directions(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

direction = Directions.RIGHT
change_to = direction

score = 0

def showScore(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()

    game_window.blit(score_surface, score_rect)

def gameOver():
    my_font = pygame.font.SysFont('times new roman', 50)
    
    game_over_surface = my_font.render('Your Score is : ' + str(score), True, red)
    
    game_over_rect = game_over_surface.get_rect()
    
    game_over_rect.midtop = (window_x/2, window_y/4)
    
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    
    time.sleep(2)
    
    pygame.quit()

    quit()

def oppositeDirection(curr_dir):
    return (curr_dir.value + 2) % 4

def snakeHitBorder():
    return snake_pos[0] < 0 or snake_pos[0] > window_x - 10 or snake_pos[1] < 0 or snake_pos[1] > window_y - 10

def isOverlapping(i1, i2):
    return (i1[0] == i2[0]) and (i1[1] == i2[1])

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_UP:
                    change_to = Directions.UP
                case pygame.K_DOWN:
                    change_to = Directions.DOWN
                case pygame.K_LEFT:
                    change_to = Directions.LEFT
                case pygame.K_RIGHT:
                    change_to = Directions.RIGHT

    direction = change_to if oppositeDirection(change_to) != direction.value else direction

    changed_axis = direction.value % 2
    displacement = -10 if direction.value < 2 else 10
    
    snake_pos[changed_axis] += displacement

    snake_body.insert(0, list(snake_pos))

    # If head of snake overlaps with the fruit
    if isOverlapping(snake_pos, fruit_pos):
        # Increment score
        score += 10
        # Indicate a new fruit needs to be spawned
        fruit_spawn = False
        # Skip the pop, which makes the snake grow
    else:
        snake_body.pop()

    if not fruit_spawn:
        fruit_pos = newFruitSpawnLocation(window_x, window_y, snake_body)

    fruit_spawn = True
    game_window.fill(black)

    # Draw the snake body
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
    
    #Draw the fruit
    pygame.draw.rect(game_window, white, pygame.Rect(fruit_pos[0], fruit_pos[1], 10, 10))

    if snakeHitBorder():
        gameOver()
    
    for segment in snake_body[1:]:
        if isOverlapping(snake_pos, segment):
            gameOver()

    showScore(1, white, 'times new roman', 20)

    pygame.display.update()

    fps.tick(player_speed)