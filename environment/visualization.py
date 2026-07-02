import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import os
from dotenv import load_dotenv
from environment.movement import get_random_direction, get_direction_delta

load_dotenv()


class Environment:
    def __init__(self, width=10, height=10, num_predators=1, num_preys=1):
        self.width = width
        self.height = height
        self.predators = [{'x': random.uniform(0, width), 'y': random.uniform(0, height)} for _ in range(num_predators)]
        self.preys = [{'x': random.uniform(0, width), 'y': random.uniform(0, height)} for _ in range(num_preys)]
    
    def set_predator_position(self, index, x, y):
        """Set position of a specific predator"""
        if 0 <= index < len(self.predators):
            self.predators[index]['x'] = max(0, min(self.width, x))
            self.predators[index]['y'] = max(0, min(self.height, y))
    
    def set_prey_position(self, index, x, y):
        """Set position of a specific prey"""
        if 0 <= index < len(self.preys):
            self.preys[index]['x'] = max(0, min(self.width, x))
            self.preys[index]['y'] = max(0, min(self.height, y))


class Visualizer:
    def __init__(self, env, update_callback=None, movement_interval=1000):
        self.env = env
        self.update_callback = update_callback
        self.movement_interval = movement_interval
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.ax.set_xlim(-1, env.width + 1)
        self.ax.set_ylim(-1, env.height + 1)
        self.ax.set_aspect('equal')
        self.ax.set_title('Predator-Prey Environment')
        
        # Draw boundary wall
        wall = plt.Rectangle(
            (0, 0), 
            env.width, 
            env.height, 
            fill=False, 
            edgecolor='black', 
            linewidth=3
        )
        self.ax.add_patch(wall)
        
        # Create predator patches (red triangles)
        self.predator_patches = []
        for _ in self.env.predators:
            patch = plt.Polygon(
                [[0, 0], [-0.3, -0.3], [0.3, -0.3]], 
                color='red', 
                label='Predator' if not self.predator_patches else None
            )
            self.ax.add_patch(patch)
            self.predator_patches.append(patch)
        
        # Create prey patches (green circles)
        self.prey_patches = []
        for _ in self.env.preys:
            patch = plt.Circle(
                (0, 0), 
                0.2, 
                color='green', 
                label='Prey' if not self.prey_patches else None
            )
            self.ax.add_patch(patch)
            self.prey_patches.append(patch)
        
        if self.env.predators or self.env.preys:
            self.ax.legend(bbox_to_anchor=(1, 1.02), loc='lower right', borderaxespad=0)
        
    def animate(self, frame):
        if self.update_callback:
            self.update_callback(self.env)
        
        # Update predator positions
        for i, predator in enumerate(self.env.predators):
            self.predator_patches[i].set_xy([
                [predator['x'], predator['y'] + 0.3],
                [predator['x'] - 0.3, predator['y'] - 0.3],
                [predator['x'] + 0.3, predator['y'] - 0.3]
            ])
        
        # Update prey positions
        for i, prey in enumerate(self.env.preys):
            self.prey_patches[i].set_center((prey['x'], prey['y']))
        
        return self.predator_patches + self.prey_patches
    
    def start(self):
        ani = animation.FuncAnimation(
            self.fig, 
            self.animate, 
            frames=200, 
            interval=self.movement_interval, 
            blit=True
        )
        plt.show()


def main():
    # Read from .env file
    grid_width = int(os.getenv('GRID_WIDTH', '10'))
    grid_height = int(os.getenv('GRID_HEIGHT', '10'))
    num_predators = int(os.getenv('NUM_PREDATORS', '1'))
    num_preys = int(os.getenv('NUM_PREYS', '1'))
    movement_interval = int(os.getenv('MOVEMENT_INTERVAL', '1000'))
    
    env = Environment(width=grid_width, height=grid_height, num_predators=num_predators, num_preys=num_preys)
    
    # Default random movement callback if no model provided
    def random_movement(env):
        for i, predator in enumerate(env.predators):
            direction = get_random_direction()
            dx, dy = get_direction_delta(direction)
            new_x = predator['x'] + dx
            new_y = predator['y'] + dy
            env.set_predator_position(i, new_x, new_y)
        
        for i, prey in enumerate(env.preys):
            direction = get_random_direction()
            dx, dy = get_direction_delta(direction)
            new_x = prey['x'] + dx
            new_y = prey['y'] + dy
            env.set_prey_position(i, new_x, new_y)
    
    viz = Visualizer(env, update_callback=random_movement, movement_interval=movement_interval)
    viz.start()


if __name__ == "__main__":
    main()
