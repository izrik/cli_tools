#!/usr/bin/env python3

"""Read in paragraphs from STDIN and re-format them to the desired width"""

import argparse
import sys
from typing import List


class WordList:
    words = []
    _length = None

    def __init__(self, indent, margin):
        self.words = []
        self._length = None
        self.indent = indent or ''
        self.margin = margin or ''

    def format_line(self, first):
        line_out = self.margin
        if first:
            line_out += self.indent
        line_out += ' '.join(self.words)
        return line_out

    def get_length(self, first):
        if self._length is None:
            if not self.words:
                self._length = 0
            else:
                word_lengths = sum(len(_) for _ in self.words)
                self._length = word_lengths + len(self.words) - 1
            self._length += len(self.margin)
            if first:
                self._length += len(self.indent)
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


def str_or_num_spaces(value):
    try:
        value = int(value)
        return ' ' * value
    except ValueError:
        pass
    value = str(value)
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='?')
    parser.add_argument('-w', '--width', default=76, type=int)
    parser.add_argument('-s', '--string')
    parser.add_argument(
        '-i', '--indent', default=0, type=str_or_num_spaces,
        help='A string to prepend to the first line, or number of spaces to'
             'prepend. The indent is applied after any margin. Defaults to'
             'zero.')
    parser.add_argument(
        '-m', '--margin', default=0, type=str_or_num_spaces,
        help='String to prepend to each line, or the number of spaces to'
             'prepend. Defaults to zero.')
    parser.add_argument(
        '-r', '--remove-margin', default=None, type=str_or_num_spaces,
        help='String to remove from the beginning of each line of input. '
             'Defaults to nothing.')
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
    indent = args.indent
    margin = args.margin
    remove_margin = args.remove_margin
    current_words = WordList(indent, margin)
    first = True
    for line in source.readlines():
        if remove_margin and line.startswith(remove_margin):
            line = line[len(remove_margin):]
        if line == '\n' or line == '':
            print(current_words.format_line(first))
            current_words.clear()
            first = False
            continue
        ends_with_newline = line.endswith('\n')
        end = '\n' if ends_with_newline else ''
        words = line.split()
        for word in words:
            if current_words.get_length(first) + len(word) + 1 > width:
                print(current_words.format_line(first))
                current_words.clear()
                first = False
            current_words.append(word)
    if current_words:
        print(current_words.format_line(first), end=end)
        current_words.clear()


if __name__ == '__main__':
    main()
