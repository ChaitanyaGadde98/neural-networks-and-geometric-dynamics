"""
Movement direction map for discrete movement steps
"""
import random

# Movement directions: (dx, dy)
MOVEMENT_DIRECTIONS = {
    'U': (0, 1),      # Up
    'D': (0, -1),     # Down
    'L': (-1, 0),     # Left
    'R': (1, 0),      # Right
    'LU': (-1, 1),    # Left-Up
    'LD': (-1, -1),   # Left-Down
    'RU': (1, 1),     # Right-Up
    'RD': (1, -1),    # Right-Down
}

DIRECTION_NAMES = list(MOVEMENT_DIRECTIONS.keys())



def get_direction_delta(direction):
    """Get the (dx, dy) delta for a given direction"""
    return MOVEMENT_DIRECTIONS.get(direction, (0, 0))
