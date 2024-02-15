#!/usr/bin/env python3

import argparse
import random


SOURCE = '''
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
non proident, sunt in culpa qui officia deserunt mollit anim id est
laborum.
'''

WORDS = SOURCE.split()
LEN = len(WORDS)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', type=int, help='Number of words to generate',
                        default=LEN)
    parser.add_argument('--skip', '-s', type=int, default=0,
                        help='Number of words to skip before iterating from '
                             'the list.')
    parser.add_argument('--skip-random', '-r', action='store_true',
                        help='Skip a random number of words before iterating '
                             'from the list')
    args = parser.parse_args()

    skip = 0
    if args.skip_random:
        skip = random.randint(0, LEN)
    elif args.skip:
        skip = args.skip

    words_to_print = []
    for i in range(args.w):
        words_to_print.append(WORDS[(i+skip)%LEN])

    print(' '.join(words_to_print))

if __name__ == '__main__':
    main()


