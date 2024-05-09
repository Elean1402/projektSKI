from timeit import repeat
import platform


def benchmark(func):
    txt = open("benchmark.txt", "a")
    zug_time = min(repeat(func, repeat=100, number=1000))
    #txt.write("PC Specs"+platform.machine()+platform.system()+platform.processor() + "\n")
    txt.write(str(func) + str(zug_time) + "\n")

