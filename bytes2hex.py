#!/usr/bin/env python3
import argparse
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ignore-invalid', action='store_true')
    parser.add_argument('file', nargs='?')
    args = parser.parse_args()
    file = args.file
    if file is None or file == '-':
        fd = sys.stdin.buffer
    else:
        fd = open(file, 'rb')
    first = True
    while ch := fd.read(1):
        if not first:
            print(' ', end='')
        first = False
        print(f'{int.from_bytes(ch):02x}', end='')


if __name__ == '__main__':
    main()
