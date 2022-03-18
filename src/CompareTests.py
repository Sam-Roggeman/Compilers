import filecmp
import sys


def main(argv):
    try:
        f1 = argv[0]
        f2 = argv[1]
        result = filecmp.cmp(f1, f2, shallow=False)
        print(result)
    except FileNotFoundError as error:
        print("FileException")
        print(error, file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
