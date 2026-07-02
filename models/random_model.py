"""
Model 1: Single Predator - Single Prey with Random Movement
"""
import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from environment.visualization import Environment, Visualizer
from environment.movement import DIRECTION_NAMES, get_direction_delta
from dotenv import load_dotenv

load_dotenv()


def random_movement(env):
    """Movement logic for model 1: random discrete movement"""
    for i, predator in enumerate(env.predators):
        direction = random.choice(DIRECTION_NAMES)
        dx, dy = get_direction_delta(direction)
        new_x = predator['x'] + dx
        new_y = predator['y'] + dy
        env.set_predator_position(i, new_x, new_y)
    
    for i, prey in enumerate(env.preys):
        direction = random.choice(DIRECTION_NAMES)
        dx, dy = get_direction_delta(direction)
        new_x = prey['x'] + dx
        new_y = prey['y'] + dy
        env.set_prey_position(i, new_x, new_y)


def run_model_1():
    """Run model 1 with one predator and one prey"""
    print("Starting Model 1: Single Predator - Single Prey with Random Movement")
    
    # Read from .env file
    grid_width = int(os.getenv('GRID_WIDTH', '10'))
    grid_height = int(os.getenv('GRID_HEIGHT', '10'))
    num_predators = int(os.getenv('NUM_PREDATORS', '1'))
    num_preys = int(os.getenv('NUM_PREYS', '1'))
    movement_interval = int(os.getenv('MOVEMENT_INTERVAL', '1000'))
    
    env = Environment(width=grid_width, height=grid_height, num_predators=num_predators, num_preys=num_preys)
    viz = Visualizer(env, update_callback=random_movement, movement_interval=movement_interval)
    viz.start()


if __name__ == "__main__":
    run_model_1()
