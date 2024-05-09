from timeit import repeat

from src import zuggenerator
from zuggenerator import *


def benchmark(func):
    txt = open("benchmark.txt", "a")
    zug_time: float = min(repeat(func, repeat=5, number=1000))
    txt.write(str(func) + str(zug_time) + "\n")


benchmark(alpha_generation())