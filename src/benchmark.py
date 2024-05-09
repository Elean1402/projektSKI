from timeit import repeat


def benchmark(func):
    txt = open("benchmark.txt", "a")
    print(str(func))
    zug_time = min(repeat(func, repeat=100, number=1000))
    print(str(zug_time))
    txt.write(str(func) + str(zug_time) + "\n")
