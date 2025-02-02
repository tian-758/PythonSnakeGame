import random
from enum import Enum

def newFruitSpawnLocation(window_size_x, window_size_y, snake_positions):

    x = random.randrange(1, window_size_x//10) * 10
    y = random.randrange(1, window_size_y//10) * 10

    return [x, y]

class Directions(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

class Snake:
    def __init__(self, x_boundary, y_boundary, initial_position, initial_direction, initial_length):
        self.window_x = x_boundary
        self.window_y = y_boundary
        
        self.pos = initial_position

        self.direction = Directions.RIGHT

        match initial_direction.upper():
            case "LEFT":
                self.direction = Directions.LEFT
            case "RIGHT":
                self.direction = Directions.RIGHT
            case "UP":
                self.direction = Directions.UP
            case "DOWN":
                self.direction = Directions.DOWN

        self.body = [self.pos]

        changed_axis = self.direction.value % 2
        displacement = 10 if self.direction.value < 2 else -10

        for _ in range(initial_length - 1):
            next_segment = [self.body[-1][0], self.body[-1][1]]
            next_segment[changed_axis] += displacement

            self.body.add(self.direction.value % 2)

    def MetGameOverConditions(self):
        return False
