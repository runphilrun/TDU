import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='Process some stuff.')
    parser.add_argument('integers', help='an integer for the accumulator',
        type=int,
        metavar='N',
        nargs='+')
    parser.add_argument('--sum', help='sum the integers (default: find the max)',
        dest='accumulate',
        action='store_const',
        const=sum,
        default=max)

    args = parser.parse_args()

if __name__ == "__main__":
    main()
