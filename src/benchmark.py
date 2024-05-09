from timeit import repeat


def benchmark(func):
    txt = open("benchmark.txt", "a")
    zug_time = min(repeat(func, repeat=100, number=1000))
    txt.write(str(func) + str(zug_time) + "\n")

