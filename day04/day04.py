#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import defaultdict


def parse_line(line):
    parts = line.split('|')
    card_numbers = set(int(n) for n in parts[0].split(':')[1].strip().split(' ') if n)
    my_numbers = set(int(n) for n in parts[1].strip().split())
    return card_numbers, my_numbers


def read_input(input_file):
    return [parse_line(ln)
            for ln in open(input_file).read().rstrip().split('\n')]


def part1(inp):
    sum = 0
    for c, m in inp:
        win = c & m
        if win:
            sum += (1 << (len(win) - 1))
    return sum


def part2(lines):
    numbers = [1] * len(lines)
    for i, (c, m) in enumerate(lines):
        win = len(c & m)
        for n in range(i + 1, i + win + 1):
            numbers[n] += numbers[i]
    return sum(numbers)


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
