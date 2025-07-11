#!/usr/bin/env python3
import argparse
import os
import re
import sys


def main():
    parser = argparse.ArgumentParser(
        description='Apply regular expressions to stadndard input.')
    parser.add_argument('pattern')
    parser.add_argument('replacement', nargs='?')
    args = parser.parse_args()
    pattern = re.compile(args.pattern)
    replacement = args.replacement
    for line in sys.stdin:
        has_newline = line.endswith('\n')
        line = line.replace('\n','')
        if replacement:
            line = pattern.sub(replacement, line)
        else:
            m = pattern.search(line)
            if m:
                line = m[0]
            else:
                line = None
        end = '\n' if has_newline else ''
        if line is not None:
            print(line, end=end)


if __name__ == '__main__':
    main()
