import os
import sys
import json
import numpy as np
import cProfile
import pstats
from typing import Callable, Any, Dict, List, Tuple
from tabulate import tabulate
from io import StringIO
from timeit import repeat
from types import MappingProxyType
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.moveLib import MoveLib



from src.moveGenerator import MoveGenerator1
from src.gui import Gui
from src.alpha_beta_Kopie import AlphaBetaSearch
from src.gamestate import GameState
from src.model import Player, DictMoveEntry
from src.board_final import Board

# Ensure the data directories exist
if not os.path.exists('data/benchmarks'):
    os.makedirs('data/benchmarks')

if not os.path.exists('data/profiles'):
    os.makedirs('data/profiles')

def convert_to_serializable(obj, seen=None):
    if seen is None:
        seen = set()
    
    obj_id = id(obj)
    if obj_id in seen:
        return f"<Circular reference to object {obj_id}>"

    seen.add(obj_id)

    if isinstance(obj, (np.integer, int)):
        return int(obj)
    elif isinstance(obj, (np.floating, float)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (dict, MappingProxyType)):
        return {k: convert_to_serializable(v, seen) for k, v in obj.items()}
    elif hasattr(obj, '__dict__'):
        return {k: convert_to_serializable(v, seen) for k, v in obj.__dict__.items()}
    elif hasattr(obj, '__class__') and hasattr(obj, '__slots__'):
        return {slot: convert_to_serializable(getattr(obj, slot), seen) for slot in obj.__slots__}
    elif callable(obj):
        return str(obj)
    else:
        return str(obj)

def lightweight_warmup():
    """A lightweight function that mimics some operations of the main functions."""
    for i in range(1000):
        x = np.random.rand(100)
        x = np.sort(x)
    return np.sum(x)

def benchmark(func_with_args: Callable[[], Tuple[Any, int]], func_name: str = "", fen: str = None, repetitions: int = 1, depth: int = 0, move_output: bool = False, include_move_count: bool = False, include_output: bool = True, warmup_reps: int = 10) -> List[Dict[str, Any]]:
    results = []

    def wrapper():
        if include_move_count:
            return func_with_args()
        else:
            return func_with_args(), None

    # Warmup phase
    for _ in range(warmup_reps):
        lightweight_warmup()

    # Timing phase
    times = repeat(wrapper, repeat=repetitions, number=1)
    mean_duration = sum(times) / repetitions

    # Only call wrapper if output or move_count is needed
    output, move_count = None, None
    if include_output or include_move_count:
        output, move_count = wrapper()

    if move_output:
        if output is None:
            output = "No valid move found."

    result = {
        "function_name": func_name,
        "fen": fen,
        "depth": depth,
        "mean_duration": mean_duration,
    }

    if include_output:
        result["output"] = output

    if include_move_count:
        result["move_count"] = move_count

    results.append(result)

    # Save results to files named after the function
    text_file_path = f'data/benchmarks/{func_name}_benchmark_results.txt'
    json_file_path = f'data/benchmarks/{func_name}_benchmark_results.json'

    with open(text_file_path, 'a') as text_file:
        text_file.write(tabulate(results, headers="keys", tablefmt="grid"))
        text_file.write("\n")

    existing_data = []
    if os.path.exists(json_file_path):
        try:
            with open(json_file_path, 'r') as json_file:
                existing_data = json.load(json_file)
        except json.JSONDecodeError:
            print(f"Warning: JSON file {json_file_path} is corrupted or not in the correct format. A new file will be created.")
    
    existing_data.extend(results)

    with open(json_file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4, default=convert_to_serializable)
    
    return results

def profile(func_with_args: Callable[[], Tuple[Any, int]], func_name: str = "", fen: str = None, repetitions: int = 1, depth: int = 0, move_output: bool = False, include_move_count: bool = False, include_output: bool = True, warmup_reps: int = 10) -> None:
    profiler = cProfile.Profile()

    def wrapper():
        if include_move_count:
            return func_with_args()
        else:
            return func_with_args(), None

    # Warmup phase
    for _ in range(warmup_reps):
        lightweight_warmup()

    profiler.enable()
    times = repeat(wrapper, repeat=repetitions, number=1)
    profiler.disable()

    mean_duration = sum(times) / repetitions

    # Only call wrapper if output or move_count is needed
    output, move_count = None, None
    if include_output or include_move_count:
        output, move_count = wrapper()

    if move_output:
        if output is not None:
            if(isinstance(output[0],np.uint64)):
                output = [MoveLib.BitsToPosition(output[0]), MoveLib.BitsToPosition(output[1])]
        else:
            output = "No valid move found."

    s = StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats(pstats.SortKey.TIME)
    ps.print_stats()

    profile_output = s.getvalue()

    profile_text_file_path = f"data/profiles/{func_name}_profile.txt"
    with open(profile_text_file_path, 'w') as f:
        f.write(profile_output)
        f.write(f"\nMean duration over {repetitions} repetitions: {mean_duration} seconds\n")

        if include_output:
            f.write(f"Output: {output}\n")

        if include_move_count:
            f.write(f"Move count: {move_count}\n")

    profile_pstats_file_path = f"data/profiles/{func_name}_profile.pstats"
    profiler.dump_stats(profile_pstats_file_path)

    print(f"Profile results saved to {profile_text_file_path} and {profile_pstats_file_path}")
