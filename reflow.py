#!/usr/bin/env python3

"""Read in paragraphs from STDIN and re-format them to the desired width"""

import argparse
import sys
from typing import List


class WordList:
    words = []
    _length = None

    def __init__(self):
        self.words = []
        self._length = None

    @property
    def length(self):
        if self._length is None:
            if not self.words:
                self._length = 0
            else:
                word_lengths = sum(len(_) for _ in self.words)
                self._length = word_lengths + len(self.words) - 1
        return self._length

    def append(self, value):
        self.words.append(value)
        self._length = None

    def clear(self):
        self.words.clear()
        self._length = None

    def __iter__(self):
        return iter(self.words)

    def __bool__(self):
        return not not self.words


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='?')
    parser.add_argument('-w', '--width', default=76, type=int)
    parser.add_argument('-s', '--string')
    args = parser.parse_args()
    file = args.file
    if args.string:
        from io import StringIO
        source = StringIO(args.string)
    elif not file or file == '-':
        source = sys.stdin
    else:
        source = open(file)
    width = args.width
    current_words = WordList()
    for line in source.readlines():
        if line == '\n' or line == '':
            print(' '.join(current_words))
            current_words.clear()
            continue
        ends_with_newline = line.endswith('\n')
        end = '\n' if ends_with_newline else ''
        words = line.split()
        for word in words:
            if current_words.length + len(word) + 1 > width:
                print(' '.join(current_words))
                current_words.clear()
            current_words.append(word)
    if current_words:
        print(' '.join(current_words), end=end)
        current_words.clear()


if __name__ == '__main__':
    main()
