from timeit import repeat
import cProfile
import pstats
import io
from statistics import mean
class Benchmark:
    @staticmethod
    def benchmark(func_with_args, func_name="", fen=None, repetitions=1000):
        """
        Inputs: func_with_args is the function to be benchmarked with its arguments,
                func_name is the name of the function as string (optional),
                fen is the fen string (optional)
        Output: writes the benchmark results to a file
        
        Example: Benchmark.benchmark(lambda: my_function('arg1_value', 'arg2_value'), 'my_function', 'fen_string')
        """

        with open("benchmark1.txt", "a") as txt:
            zug_time = (repeat(func_with_args, number=repetitions, repeat=1000))
            zug_time = mean(zug_time)
            if fen:
                txt.write(f'{func_name} für {fen} ist {zug_time}s (min aus {repetitions} Zügen) \n')
            else:
                txt.write(f'{func_name} ist {zug_time}s (min aus {repetitions} Zügen) \n')


    @staticmethod
    def profile(func_with_args, func_name="", sortby='tottime', mode='text'):
        """
        Inputs: func_with_args is the function to be profiled with its arguments,
                func_name is the name of the function as string (optional),
                sortby is the sorting criteria for the profile output (optional, default is 'cumulative')
        Output: writes the profile results to a file

        Example: Benchmark.profile(lambda: my_function('arg1_value', 'arg2_value'), 'my_function', 'time')
        """

        pr = cProfile.Profile()
        pr.enable()

        # Call the function here
        func_with_args()

        pr.disable()
        if mode == 'text':
            s = io.StringIO()
            ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
            ps.print_stats()
            with open(f"{func_name}_profile.txt", "w") as txt:
                txt.write(f'Profile results for {func_name}:\n')
                txt.write(s.getvalue())
        elif mode == 'pstats':
            pr.dump_stats(f'{func_name}_profile.pstats')
        else:
            raise ValueError("Invalid mode. Choose 'text' or 'pstats'.")
