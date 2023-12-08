#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import itertools
import math

def parse_line(line):
    return line


def read_input(input_file):
    steps, nbs = open(input_file).read().rstrip().split('\n\n')
    d = {n[:3] : (n[7:10], n[12:15]) for n in nbs.split('\n')}
    return list(steps), d

def part1(steps, nbs):
    n = 'AAA'
    tot = 0
    for s in itertools.cycle(steps):
        if n == 'ZZZ':
            return tot
        tot += 1
        if s == 'L':
            ind = 0
        else:
            ind = 1
        n = nbs[n][ind] 
    return tot

def search(steps, first, nbs):
    n = first
    tot = 0
    for s in itertools.cycle(steps):
        if n[2] == 'Z':
            return tot
        tot += 1
        if s == 'L':
            ind = 0
        else:
            ind = 1
        n = nbs[n][ind] 
    return tot

def part2(steps, nbs):
    gcm = 0
    for node in nbs:
        if node[2] == 'A':
            s = search(steps, node, nbs)
            if gcm == 0:
                gcm = s
            else:
                gcm = (s * gcm) // math.gcd(gcm, s)
    return gcm

def main(input_file):
    steps, nbs = read_input(input_file)

    print(part1(steps, nbs))
    print(part2(steps, nbs))


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'input'

    main(input_file)

# vim: sts=4:ts=4:et:sw=4:number:
