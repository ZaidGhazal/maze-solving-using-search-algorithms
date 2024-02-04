
"""This module contains the Maze implementation"""
from typing import List, Tuple

import numpy as np


class Maze:
    """Class to represent a maze from a numpy array"""
    def __init__(self, maze_size: Tuple[int, int], start: Tuple[int, int], goal: Tuple[int, int], obsticles_desity: float = 0.15):
        self.maze_size = maze_size
        self.start = start
        self.goal = goal
        self.obsticles_desity = obsticles_desity

        self._create_maze()

    def _create_maze(self):
        """Create the maze from the numpy array"""
        number_of_obsticles = int(self.maze_size[0] * self.maze_size[1] * self.obsticles_desity) 
        x_low, x_high = 0, self.maze_size[0] # x_low and x_high are the min and max values of the x coordinate.
        y_low, y_high = 0, self.maze_size[1] # y_low and y_high are the min and max values of the y coordinate. 

        ## Create the obsticles. x and y are the coordinates of the obsticles
        self.obsticles = [(np.random.randint(x_low, x_high), np.random.randint(y_low, y_high)) for _ in range(number_of_obsticles)]
        self.obsticles = [obsticle for obsticle in self.obsticles if obsticle != self.start and obsticle != self.goal]
        self.current_location =  self.start
        
    def get_current_location(self) -> Tuple[int, int]:
        """Return the current location of the agent"""
        return self.current_location
    
    def set_new_current_location(self, new_location: Tuple[int, int]):
        """Set the new location of the agent"""
        self.current_location = new_location

    def get_current_available_neighbors_locations(self, location: Tuple[int, int] = None) -> List[Tuple[int, int]]:
        """Return the neighbors of the current location of the agent"""
        x, y = location
        left_neighbor = (x - 1, y) if x - 1 >= 0 else None
        right_neighbor = (x + 1, y) if x + 1 < self.maze_size[0] else None
        up_neighbor = (x, y + 1) if y + 1 < self.maze_size[1] else None
        down_neighbor = (x, y - 1) if y - 1 >= 0 else None
        neighbors = [left_neighbor, right_neighbor, up_neighbor, down_neighbor]

        return [neighbor for neighbor in neighbors if neighbor not in self.obsticles and neighbor is not None]
    
    def get_start_location(self) -> Tuple[int, int]:
        """Return the start location"""
        return self.start
    
    def get_goal_location(self) -> Tuple[int, int]:
        """Return the goal location"""
        return self.goal
    
    def is_goal_reached(self) -> bool:
        """Return True if the current location is the goal"""
        return self.current_location == self.goal
    
    def is_two_locations_connected(self, location1: Tuple[int, int], location2: Tuple[int, int]) -> bool:
        """Return True if the two locations are connected"""
        return location2 in self.get_current_available_neighbors_locations(location1) or location1 == location2
