#!/usr/bin/env python3.12
# -*- coding: utf-8 -*-
import os.path
import sys

sys.path.insert(0, os.path.abspath(os.path.join(__file__, '..', '..')))
import aoc

def parse_line(line):
    return line


def read_input(input_file):
    return [parse_line(ln)
            for ln in open(input_file).read().rstrip().split('\n')]


def part1(inp):
    pass


def part2(inp):
    pass


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
