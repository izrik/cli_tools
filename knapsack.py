#!/usr/bin/env python3

import argparse
from itertools import combinations, chain


def powerset(iterable):
    """powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"""
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('target', type=float)
    parser.add_argument('items', nargs='+', type=float)
    args = parser.parse_args()
    target = args.target
    items = args.items
    best = None
    best_sum = 0
    for s in powerset(items):
        s_sum = sum(s)
        if best is None or (best_sum < s_sum <= target):
            best = s
            best_sum = s_sum
            print(f'{best_sum:g} = {" + ".join(str(_) for _ in best)}')
    if best is None:
        print('Found nothing, somehow')
    else:
        print(f'{best_sum:g} = {" + ".join(str(_) for _ in best)}')


if __name__ == '__main__':
    main()
