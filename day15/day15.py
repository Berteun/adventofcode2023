#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import defaultdict


def read_input(input_file):
    return open(input_file).read().rstrip().split(',')


def shash(s):
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h %= 256
    return h


def part1(inp):
    return sum(shash(s) for s in inp)


def part2(inp):
    d = defaultdict(list)

    for s in inp:
        if s[-1] == '-':
            label = s[:-1]
            focal = None
        else:
            label, focal = s.split('=')

        h = shash(label)
        for i in range(len(d[h])):
            if d[h][i][0] == label:
                if focal is None:
                    d[h].pop(i)
                else:
                    d[h][i] = (label, focal)
                break
        else:
            if focal is not None:
                d[h].append((label, focal))

    total = 0
    for box, lenses in d.items():
        total += (box + 1) * sum(int(l[1]) * (i + 1) for i, l in enumerate(lenses))
    return total


def main(input_file):
    inp = read_input(input_file)

    print(part1(inp))
    print(part2(inp))


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'input'

    main(input_file)

# vim: sts=4:ts=4:et:sw=4:number:
