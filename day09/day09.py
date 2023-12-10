#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def parse_line(line):
    return [int(i) for i in line.split(' ')]

def read_input(input_file):
    return [parse_line(ln)
            for ln in open(input_file).read().rstrip().split('\n')]


def deltas(l):
    return [l[i] - l[i-1] for i in range(1, len(l))]

def extrapolate(l):
    d = deltas(l)
    if set(d) == set([0]):
        return l[-1]
    else:
        return l[-1] + extrapolate(d)

def part1(inp):
    s = 0
    for l in inp:
        s += extrapolate(l)
    return s

def extrapolatebw(l):
    d = deltas(l)
    if set(d) == set([0]):
        return l[0]
    else:
        res = l[0] - extrapolatebw(d)
        return res

def part2(inp):
    s = 0
    for l in inp:
        s += extrapolatebw(l)
    return s



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
