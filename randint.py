#!/usr/bin/env python3

from random import randint
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('a', type=int, nargs='?')
    parser.add_argument('b', type=int, nargs='?')
    parser.add_argument('--count', '-c', type=int)
    parser.add_argument('--zero-pad', '-z', action='store_true')
    args = parser.parse_args()
    print(args)
    a = args.a
    b = args.b
    c = args.count
    if not c:
        c = 1
    if c < 1:
        c = 1

    start = 0
    end = 100
    if a is not None:
        if b is not None:
            start = a
            end = b
        else:
            start = 0
            end = a
    L = len(str(b))
    fmt = f'{{:0{L}}}'

    for i in range(c):
        s = randint(a, b)
        if args.zero_pad:
            s = fmt.format(s).format()
        print(s)

if __name__ == '__main__':
    main()

