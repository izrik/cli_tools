#!/usr/bin/env python3
import argparse
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ignore', '-i')
    parser.add_argument('file', nargs='?')
    args = parser.parse_args()
    ignore = args.ignore or ''
    file = args.file
    if file is None or file == '-':
        fd = sys.stdin
    else:
        fd = open(file)
    digits = '0123456789abcdef'
    out = sys.stdout.buffer
    while True:
        ch1 = fd.read(1)
        if ch1 is None or ch1 == '':
            break
        if ch1 in ' \t\r\n' or ch1 in ignore:
            continue
        if ch1 not in '0123456789abcdefABCDEF':
            raise Exception(f'Invalid character "{ch1}"')
        ch1 = ch1.lower()
        ch2 = fd.read(1)
        if ch2 is None or ch2 == '':
            break
        if ch2 not in '0123456789abcdefABCDEF':
            raise Exception(f'Invalid character "{ch2}"')
        ch2 = ch2.lower()
        b = digits.index(ch1) * 16 + digits.index(ch2)
        out.write(b.to_bytes())


if __name__ == '__main__':
    main()
