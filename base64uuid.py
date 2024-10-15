#!/usr/bin/env python3

import argparse
import base64
import binascii
import sys
import uuid


def decode(file):
    if file is None or file == '-':
        fd = sys.stdin
    else:
        fd = open(file)
    while line := fd.readline():
        raw = base64.b64decode(line)
        if len(raw) < 16:
            raise Exception("Not enough bytes")
        if len(raw) > 16:
            print("Warning: too many bytes", file=sys.stderr)
        fmt = '{0:02x}'
        out = (
            fmt.format(raw[0]) +
            fmt.format(raw[1]) +
            fmt.format(raw[2]) +
            fmt.format(raw[3]) +
            '-' +
            fmt.format(raw[4]) +
            fmt.format(raw[5]) +
            '-' +
            fmt.format(raw[6]) +
            fmt.format(raw[7]) +
            '-' +
            fmt.format(raw[8]) +
            fmt.format(raw[9]) +
            '-' +
            fmt.format(raw[10]) +
            fmt.format(raw[11]) +
            fmt.format(raw[12]) +
            fmt.format(raw[13]) +
            fmt.format(raw[14]) +
            fmt.format(raw[15])
        )
        print(out)


def encodebytes(s):
    """Encode a bytestring into a bytes object containing multiple lines
    of base-64 data."""
    base64._input_type_check(s)
    pieces = []
    for i in range(0, len(s), base64.MAXBINSIZE):
        chunk = s[i : i + base64.MAXBINSIZE]
        pieces.append(binascii.b2a_base64(chunk, newline=False))
    return b"".join(pieces)

def encode(file):
    if file is None or file == '-':
        fd = sys.stdin
    else:
        fd = open(file)
    while line := fd.readline():
        u = uuid.UUID(hex=line)
        out = encodebytes(u.bytes)
        print(out.decode())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--decode', '-d', action='store_true')
    parser.add_argument('file', nargs='?')
    args = parser.parse_args()
    file = args.file
    if args.decode:
        decode(file)
    else:
        encode(file)


if __name__ == '__main__':
    main()
