import cProfile
import io
import pstats
from statistics import mean
from timeit import repeat
import time
import cProfile
import io
import pstats

class HighPrecisionStats(pstats.Stats):
    def f8(self, x):
        return "%8.6f" % x  # Increase precision to 6 decimal places
class Benchmark:
    @staticmethod
    def benchmark(func_with_args, func_name="", fen=None, repetitions=100000):
        """
        Inputs: func_with_args is the function to be benchmarked with its arguments,
                func_name is the name of the function as string (optional),
                fen is the fen string (optional)
        Output: writes the benchmark results to a file
        
        Example: Benchmark.benchmark(lambda: my_function('arg1_value', 'arg2_value'), 'my_function', 'fen_string')
        """

        with open("benchmark1.txt", "a") as txt:
            zug_time = (repeat(func_with_args, number=1, repeat=repetitions))
            zug_time = mean(zug_time)
            if fen:
                txt.write(f'{func_name} für {fen} ist {zug_time}s (mean aus {repetitions} Zügen) \n')
            else:
                txt.write(f'{func_name} ist {zug_time}s (mean aus {repetitions} Zügen) \n')

    @staticmethod
    def profile(func_with_args, func_name="", sortby='tottime', mode='text'):
        pr = cProfile.Profile(time.perf_counter)  # Use time.perf_counter for higher precision
        pr.enable()

        # Call the function here
        func_with_args()

        pr.disable()
        if mode == 'text':
            s = io.StringIO()
            ps = HighPrecisionStats(pr, stream=s).sort_stats(sortby)  # Use HighPrecisionStats
            ps.print_stats()
            with open(f"{func_name}_profile.txt", "w") as txt:
                txt.write(f'Profile results for {func_name}:\n')
                txt.write(s.getvalue())
        elif mode == 'pstats':
            pr.dump_stats(f'{func_name}_profile.pstats')
        else:
            raise ValueError("Invalid mode. Choose 'text' or 'pstats'.")
