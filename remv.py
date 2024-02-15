#!/usr/bin/env python3
import argparse
import os
import re


def main():
    parser = argparse.ArgumentParser(
        description='Rename files via regular expression. Assumes all files '
                    'are in the current directory. Traversal to other '
                    'folders outside $PWD is undefined.')
    parser.add_argument('source')
    parser.add_argument('target')
    args = parser.parse_args()
    source = re.compile(args.source)
    target = args.target
    renames = []
    for item in os.listdir():
        if source.search(item):
            renames.append((item, source.sub(target, item)))
    maxlen = 0
    renames = sorted(renames, key=lambda a: a[0])
    for old, new in renames:
        maxlen = max(len(old), maxlen)
    for old, new in renames:
        s = ' ' * (maxlen - len(old))
        print(f'{old} {s}-> {new}')
    proceed = input('Proceed? [yN] ')
    if not proceed:
        proceed = ''
    proceed = proceed.lower()
    if proceed and proceed.startswith('y'):
        for old, new in renames:
            # TODO: check if exists
            os.rename(old, new)


if __name__ == '__main__':
    main()
