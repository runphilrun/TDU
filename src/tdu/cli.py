import sys
import argparse

def main():
    """
    ``tdu --help``
    TODO: Show help screen.

    >>> 1 + 1
    2
    """
    parser = argparse.ArgumentParser(description='Thruster Design Utility')
    parser.add_argument('config', help='thruster configuration file',
        type=str,
        metavar='N',
        nargs='+')

    args = parser.parse_args()

if __name__ == "__main__":
    main()
