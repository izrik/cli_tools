#!/usr/bin/env python3
import argparse
import sys


def get_file(filename):
    if not filename:
        return sys.stdin
    return open(filename)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--length', type=int, default=80)
    parser.add_argument('filename', nargs='?')
    args = parser.parse_args()
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line is None:
            break
        n = 0
        s = line
        while len(line) - n > args.length:
            s = line[n:n + args.length]
            print(s)
            n += args.length
        print(line[n:])


if __name__ == '__main__':
    main()
