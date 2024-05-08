from timeit import repeat

def benchmark(func: str):
    txt = open("benchmark.txt", "a")
    zug_time: float = min(repeat(func, repeat=5, number=1000))
    txt.write(func + str(zug_time) + "\n")
