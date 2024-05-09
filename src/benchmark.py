from timeit import repeat


def benchmark(fen,func):
    txt = open("benchmark.txt", "a")
    print(str(func))
    zug_time = min(repeat(func, number=1000))
    print(str(zug_time))
    func = str(func).split(" ")
    name = func[1]
    txt.write(name +" für "+fen+": "+ str(zug_time) + "\n")
