
from typing import List, Tuple

import numpy as np
from matplotlib import pyplot as plt

from src.utils.data_structures import PriorityQueue, Queue, Stack
from src.utils.maze import Maze


class AlgorithmsBase:
    def __init__(self, maze: Maze, **kwargs):
        self.maze = maze

        self.visited = set()
        self.path = []
        self.solution_path = []
        self.soultion_path_length = 0
        self.expanded_nodes = 0
        self.visualization_wait_until_close_time = kwargs.get('visualization_wait_until_close_time', 4)
        self.visualization_latency = kwargs.get('visualization_latency', 0.05)

    def run(self, visualization_latency: float = 0.05, visualization_wait_until_close_time: int = 4):
        """ Run the algorithm """
        raise NotImplementedError

    def interactive_visualization(self, figure, ax, path):
        """ Live visualization of the algorithm """

        ax.clear() # Clear previous plot
        #3 Background color is dark gray
        figure.patch.set_facecolor('#000')

        
        ax.clear()  # Clear previous plot
        ax.set_facecolor('#000')
        ax.set_xticks(np.arange(0, self.maze.maze_size[0], 1))
        ax.set_yticks(np.arange(0, self.maze.maze_size[1], 1))
        ax.set_xlim(-0.5, self.maze.maze_size[0])
        ax.set_ylim(-0.5, self.maze.maze_size[1])
        # ax.grid(color='black', linestyle='-', linewidth=0.5)

        ## For each possible location, draw a dot
        for x in range(self.maze.maze_size[0]):
            for y in range(self.maze.maze_size[1]):
                ax.plot(x, y, 'o', color='gray') if (x, y) not in self.maze.obsticles else ax.plot(x, y, 'x', color='white')

        ## For each obsticle, draw a black X
        for obsticle in self.maze.obsticles:
            ax.plot(obsticle[0], obsticle[1], 'x', color='white')


        ## Draw the path
        for i in range(len(path) - 1):
            location_1 = path[i]
            location_2 = path[i + 1]

            if not self.maze.is_two_locations_connected(location_1, location_2):
                latest_index_found_in_path = 0
                connected_loactions_to_location_2 = self.maze.get_current_available_neighbors_locations(location_2)
                for connected_location in connected_loactions_to_location_2:
                    latest_index_found_in_path = max(path[:i+1].index(connected_location), latest_index_found_in_path) if connected_location in path[:i+1] else latest_index_found_in_path

                ax.plot([location_2[0], path[latest_index_found_in_path][0]], [location_2[1], path[latest_index_found_in_path][1]], color='white')
            else:
                ax.plot([location_1[0], location_2[0]], [location_1[1], location_2[1]], color='white')

        ## Draw the current location
        ax.plot(self.maze.get_current_location()[0], self.maze.get_current_location()[1], 'o', color='yellow')
        ax.plot(self.maze.start[0], self.maze.start[1], 'o', color='green')
        ax.plot(self.maze.goal[0], self.maze.goal[1], 'o', color='red')

        title = str(self.__class__.__name__)
        ## Add space between the class name based on the capital letters
        for letter in title:
            if letter.isupper():
                title = title.replace(letter, f' {letter}')

        ax.set_title(f"{title}", color='white')
        plt.draw() # Draw the new plot
        plt.pause(self.visualization_latency)

    def highlight_solution_path(self, path: List[Tuple[int, int]], ax):
        """ Highlight the solution path """
        index = len(path) - 1
        while index > 0:
            location = path[index]
            back_location = path[index - 1]
            if self.maze.is_two_locations_connected(location, back_location):
                self.solution_path.append(location)
                index -= 1
            else:
                connected_loactions_to_location = self.maze.get_current_available_neighbors_locations(location)
                ealiest_index_found_in_path = index
                for connected_location in connected_loactions_to_location:
                    if connected_location in path and path.index(connected_location) < ealiest_index_found_in_path and connected_location not in self.solution_path:
                        ealiest_index_found_in_path = path.index(connected_location)
                
                self.solution_path.append(location)
                self.solution_path.append(path[ealiest_index_found_in_path])
                index = ealiest_index_found_in_path
        self.solution_path.append(self.maze.start)
        self.soultion_path_length = len(set(self.solution_path)) - 1
        ax.plot([location[0] for location in self.solution_path], [location[1] for location in self.solution_path], color='red', linewidth=2)



    def show_data(self, goal_reached: bool, ax):
        """ Terminate the algorithm """
        if goal_reached:
            ax.text(2, 9.25, "Solution Found!", fontsize=12, color="#00FF00")
            ax.text(0, -1, f"Solution Path Length: {self.soultion_path_length}", fontsize=12, color="#00FF00")
            ax.text(0, -1.5, f"Nodes Expanded: {self.expanded_nodes}", fontsize=12, color="#00FF00")

        else:
            ax.text(2, 9.25, "No Solution Found!", fontsize=12, color='yellow')
            ax.text(0, -1, f"Nodes Expanded: {self.expanded_nodes}", fontsize=12, color="yellow")

        timing = self.visualization_wait_until_close_time

        while timing > 0:
            ## Reset the text on (0, -2) to show the timing
            plt.pause(1)
            timing -= 1

        plt.show(block=False)
        plt.close()


class DeepFirstSearch(AlgorithmsBase):
    """Class to represent the DFS algorithm"""  
    def run(self, interactive_visualization: bool = True):
        """ Run the algorithm """
        stack = Stack()
        stack.push(self.maze.get_start_location())

        figure = plt.figure(figsize=(5, 5))
        ax = plt.gca()
        plt.ion()

        while not stack.is_empty():
            current_location = stack.pop()
            ## Check if the current location is not visited
            if current_location not in self.visited:
                self.expanded_nodes += 1
                self.maze.set_new_current_location(current_location)
                ## Add the current location to the visited set
                self.visited.add(current_location)
                
                ## Add the current location to the path
                self.path.append(current_location)
                
                ## Check if the current location is the goal and terminate the algorithm
                if self.maze.is_goal_reached():
                    self.interactive_visualization(figure, ax, self.path)
                    self.highlight_solution_path(self.path, ax)
                    self.show_data(goal_reached=True, ax=ax)
                    return True
                
                ## Add the neighbors of the current location to the stack
                for neighbor in self.maze.get_current_available_neighbors_locations(current_location):
                    stack.push(neighbor)

            
            self.interactive_visualization(figure, ax, self.path)
        self.show_data(goal_reached=False, ax=ax)
        return False
    


class BreadthFirstSearch(AlgorithmsBase):
    """Class to represent the BFS algorithm"""  
    def run(self, interactive_visualization: bool = True):
        """ Run the algorithm """
        queue = Queue()
        queue.enqueue(self.maze.get_start_location())
        figure = plt.figure(figsize=(5, 5))
        ax = plt.gca()
        ax.set_title("BFS Algorithm")
        plt.ion()

        while not queue.is_empty():
            current_location = queue.dequeue()
            ## Check if the current location is not visited
            if current_location not in self.visited:
                self.expanded_nodes += 1
                self.maze.set_new_current_location(current_location)
                ## Add the current location to the visited set
                self.visited.add(current_location)
                
                ## Add the current location to the path
                self.path.append(current_location)
                
                ## Check if the current location is the goal and terminate the algorithm
                if self.maze.is_goal_reached():
                    self.interactive_visualization(figure, ax, self.path)
                    self.highlight_solution_path(self.path, ax)
                    self.show_data(goal_reached=True, ax=ax)
                    return True
                
                ## Add the neighbors of the current location to the queue
                for neighbor in self.maze.get_current_available_neighbors_locations(current_location):
                    queue.enqueue(neighbor)

            
            self.interactive_visualization(figure, ax, self.path)
        self.show_data(goal_reached=False, ax=ax)
        return False
    
class AStarSearch(AlgorithmsBase):
    """Class to represent the A* algorithm"""  
    def run(self, interactive_visualization: bool = True):
        """ Run the algorithm """
        queue = PriorityQueue()
        queue.enqueue(self.maze.get_start_location(), self.cost(self.maze.get_start_location()))

        figure = plt.figure(figsize=(5, 5))
        ax = plt.gca()
        ax.set_title("A* Algorithm")
        plt.ion()

        while not queue.is_empty():
            current_location = queue.dequeue()
            ## Check if the current location is not visited
            if current_location not in self.visited:
                self.expanded_nodes += 1
                self.maze.set_new_current_location(current_location)
                ## Add the current location to the visited set
                self.visited.add(current_location)
                
                ## Add the current location to the path
                self.path.append(current_location)
                
                ## Check if the current location is the goal and terminate the algorithm
                if self.maze.is_goal_reached():
                    self.interactive_visualization(figure, ax, self.path)
                    self.highlight_solution_path(self.path, ax)
                    self.show_data(goal_reached=True, ax=ax)
                    return True
                
                ## Add the neighbors of the current location to the queue
                for neighbor in self.maze.get_current_available_neighbors_locations(current_location):
                    queue.enqueue(neighbor, self.cost(neighbor))

            
            self.interactive_visualization(figure, ax, self.path)
        self.show_data(goal_reached=False, ax=ax)
        return False
    

    def manhattan_distance(self, location_1: Tuple[int, int], location_2: Tuple[int, int]) -> int:
        """ Calculate the manhattan distance """
        return abs(location_1[0] - location_2[0]) + abs(location_1[1] - location_2[1])
    
    def distance_to_goal(self, location: Tuple[int, int]) -> int:
        """ Calculate the hueuristic value """
        return self.manhattan_distance(location, self.maze.goal)
    
    def distance_from_start(self, location: Tuple[int, int]) -> int:
        """ Calculate the distance from the start location """
        return self.manhattan_distance(location, self.maze.start)
    
    def cost(self, location: Tuple[int, int]) -> int:
        """ Calculate the f value """
        return self.distance_from_start(location) + self.distance_to_goal(location)