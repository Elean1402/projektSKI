from timeit import repeat


def benchmark(func, fen=""):
    txt = open("benchmark.txt", "a")
    print(str(func))
    zug_time = min(repeat(func, repeat=100, number=10000))
    print(str(zug_time))
    func = str(func).split(" ")
    name = func[1]
    txt.write(name +" für "+fen+": "+ str(zug_time) + "\n")


def benchmark(func):
    txt = open("benchmark.txt", "a")
    print(str(func))
    zug_time = min(repeat(func, repeat=100, number=1000))
    func = str(func).split(" ")
    name = func[1]
    print(str(func)+": "+ str(zug_time))
    txt.write(name +": "+ str(zug_time) + "\n")
