from benchmark import Benchmark


def my_function(arg1, arg2):
    print(arg1, arg2)


def main():
    Benchmark.benchmark(lambda:my_function('arg1_value', 'arg2_value'), 'my_function', 'fen_tstring')


if __name__ == '__main__':
    main()
