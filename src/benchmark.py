import os
import sys
import time
import json
import numpy as np
from typing import Callable, Any, Dict, List
from tabulate import tabulate
from src.moveLib import MoveLib

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.moveGenerator import MoveGenerator1
from src.gui import Gui
from src.alpha_beta_Kopie import AlphaBetaSearch
from src.benchmark import *
from src.gamestate import GameState
from src.model import Player, DictMoveEntry
from src.board_final import Board

# Ensure the data directory exists
if not os.path.exists('data'):
    os.makedirs('data')


def convert_to_serializable(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

def benchmark(func_with_args: Callable[[], Any], func_name: str = "", fen: str = None, repetitions: int = 1, depth: int = 0, move_output: bool = False) -> List[Dict[str, Any]]:
    # List to store benchmark results
    results = []

    # Benchmark the function
    for i in range(repetitions):
        start_time = time.time()
        output = func_with_args()
        end_time = time.time()

        duration = end_time - start_time
        
        if move_output:
            if output is not None:
                output = [MoveLib.BitsToPosition(output[0]), MoveLib.BitsToPosition(output[1])]
            else:
                output = "No valid move found."

        result = {
            "function_name": func_name,
            "fen": fen,
            "depth": depth,
            "duration": duration,
            "output": output
        }
        results.append(result)
    
    # Write results to text file
    with open('data/benchmark_results.txt', 'a') as text_file:
        text_file.write(tabulate(results, headers="keys", tablefmt="grid"))
        text_file.write("\n")

    # Write results to JSON file
    json_file_path = 'data/benchmark_results.json'
    existing_data = []

    if os.path.exists(json_file_path):
        try:
            with open(json_file_path, 'r') as json_file:
                existing_data = json.load(json_file)
        except json.JSONDecodeError:
            print("Warning: JSON file is corrupted or not in the correct format. A new file will be created.")
    
    existing_data.extend(results)

    with open(json_file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4, default=convert_to_serializable)
    
    return results

# Example usage
def example_function():
    # Example function to be benchmarked
    time.sleep(1)
    return np.array([12345, 67890], dtype=np.uint64)

if __name__ == "__main__":
    benchmark(lambda: example_function(), func_name="example_function", fen="sample_fen", repetitions=3, depth=5, move_output=True)
