from timeit import repeat
import cProfile
import pstats
import io

class Benchmark:
    @staticmethod
    def benchmark(func_with_args, func_name="", fen=None):
        """
        Inputs: func_with_args is the function to be benchmarked with its arguments,
                func_name is the name of the function as string (optional),
                fen is the fen string (optional)
        Output: writes the benchmark results to a file
        
        Example: Benchmark.benchmark(lambda: my_function('arg1_value', 'arg2_value'), 'my_function', 'fen_string')
        """
        with open("benchmark.txt", "a") as txt:
            zug_time = min(repeat(func_with_args, number=1000, repeat=3))
            if fen:
                txt.write(f'{func_name} für {fen} ist {zug_time}s (min aus 1000 Zügen) \n')
            else:
                txt.write(f'{func_name} ist {zug_time}s (min aus 1000 Zügen) \n')


    @staticmethod
    def profile(func_with_args, func_name=""):
        """
        Inputs: func_with_args is the function to be profiled with its arguments,
                func_name is the name of the function as string (optional)
        Output: writes the profile results to a file
        
        Example: Benchmark.profile(lambda: my_function('arg1_value', 'arg2_value'), 'my_function')
        """
        pr = cProfile.Profile()
        pr.enable()
        func_with_args()
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        with open("profile.txt", "a") as txt:
            txt.write(f'Profile results for {func_name}:\n')
            txt.write(s.getvalue())


