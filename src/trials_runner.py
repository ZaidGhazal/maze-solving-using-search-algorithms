"""This module has the trails runner."""
import os
import time
from typing import Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel

from src.utils.algorithms import (AStarSearch, BreadthFirstSearch,
                                  DeepFirstSearch)
from src.utils.maze import Maze


class TrailsRunnerParameters(BaseModel):
    """This class has the trails runner params."""
    
    number_of_trials: int
    maze_size: Tuple[int, int]
    obsticles_desity: float
    start_location: Tuple[int, int]
    goal_location: Tuple[int, int]
    visualization_latency: float 
    visualization_wait_until_close_time: int
    results_saving_directory: str


class TrailsRunner:
    """This class has the trails runner."""

    def __init__(self, parameters: TrailsRunnerParameters):
        """Initialize the trails runner."""
        self.parameters = parameters
        self.trails_reults = pd.DataFrame()
        
    def create_trial(self):
        """Create a trial."""
        maze = Maze(maze_size=self.parameters.maze_size, start=self.parameters.start_location, goal=self.parameters.goal_location, obsticles_desity=self.parameters.obsticles_desity)
        algorithms = [DeepFirstSearch(maze, visualization_latency=self.parameters.visualization_latency, visualization_wait_until_close_time=self.parameters.visualization_wait_until_close_time),
                        BreadthFirstSearch(maze, visualization_latency=self.parameters.visualization_latency, visualization_wait_until_close_time=self.parameters.visualization_wait_until_close_time),
                        AStarSearch(maze, visualization_latency=self.parameters.visualization_latency, visualization_wait_until_close_time=self.parameters.visualization_wait_until_close_time)]

        return algorithms

    def run(self):
        """Run the trails."""
        for trail_id in range(1, self.parameters.number_of_trials+1):
            print(f"Running trail {trail_id}...")
            algorithms = self.create_trial()
            for algorithm in algorithms:
                start = time.time()
                status = algorithm.run()
                end = time.time()
                execution_time = end - start
                execution_time = execution_time  - algorithm.visualization_wait_until_close_time 
                execution_time = execution_time - (algorithm.visualization_latency*algorithm.expanded_nodes) 
                execution_time = np.round(execution_time, 1)    
                algorithm_name = algorithm.__class__.__name__
                ## Add space beteween the capital letters
                algorithm_name = " ".join([x if x.islower() else f" {x}" for x in algorithm_name]).strip()
                new_record = pd.DataFrame(
                    {"Run": trail_id, 
                    "Algorithm": algorithm_name,
                    "Solution Path Length": algorithm.soultion_path_length,
                    "Nodes Expanded": algorithm.expanded_nodes, 
                    "Algorithm Execution Time": execution_time,
                    "Solution Found": status},
                    index=[0])
                self.trails_reults = pd.concat([self.trails_reults, new_record], ignore_index=True)
            
            print(f"Trail {trail_id} completed.")
            print(f"\tSolutions Path Length: DFS: {algorithms[0].soultion_path_length}, BFS: {algorithms[1].soultion_path_length}, A*: {algorithms[2].soultion_path_length}")
            print(f"\tNodes Expanded: DFS: {algorithms[0].expanded_nodes}, BFS: {algorithms[1].expanded_nodes}, A*: {algorithms[2].expanded_nodes}")
            print("-"*25, "\n")
        
        average_results = self.trails_reults.groupby("Algorithm").mean().reset_index()
        average_results["Run"] = "Average"
        self.trails_reults = pd.concat([self.trails_reults, average_results], ignore_index=True)

        ## Create the results directory if it does not exist
        if not os.path.exists(self.parameters.results_saving_directory):
            os.makedirs(self.parameters.results_saving_directory)
        
        self.trails_reults.to_csv(os.path.join(self.parameters.results_saving_directory, "trails_results.csv"), index=False)




