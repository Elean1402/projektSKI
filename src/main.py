import sys

minimum_version = (3,12)
if sys.version_info < minimum_version:
    sys.exit("You need Python 3.12")


def main():
    print("sheesh")
    


if __name__ == "__main__":
    main()
