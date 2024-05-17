from timeit import repeat


def benchmark(func,fen=""):
    txt = open("benchmark.txt", "a")
    zug_time = min(repeat(func, number=1000))
    name: list[str] = str(func).split(" ")
    txt.write(f'{name[1]} für {fen} ist {zug_time}ms pro 1000 Züge \n')
