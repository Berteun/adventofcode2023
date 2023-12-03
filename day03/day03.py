#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import defaultdict

def parse_line(line):
    return list(line)


def read_input(input_file):
    return [parse_line(ln)
            for ln in open(input_file).read().rstrip().split('\n')]


def has_symbol_nb(inp, x, y):
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            nx = x + dx
            ny = y + dy
            if 0 <= ny < len(inp) and 0 <= nx < len(inp[y]):
                if not inp[ny][nx].isdigit() and inp[ny][nx] != '.':
                    return True
    return False


def get_gear_nbs(inp, x, y):
    nbs = set()
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            nx = x + dx
            ny = y + dy
            if 0 <= ny < len(inp) and 0 <= nx < len(inp[y]):
                if inp[ny][nx] == '*':
                    nbs.add((nx, ny))
    return nbs


def part1(inp):
    sum = 0
    for y, row in enumerate(inp):
        cur_num = 0
        symbol_nb = False
        for x, char in enumerate(row):
            if char.isdigit():
                cur_num *= 10
                cur_num += int(char)
                symbol_nb = symbol_nb or has_symbol_nb(inp, x, y)
            else:
                if symbol_nb:
                    sum += cur_num
                cur_num = 0
                symbol_nb = False
        # End of row
        if symbol_nb:
            sum += cur_num
    return sum


def part2(inp):
    gear_to_nbs = defaultdict(set)
    for y, row in enumerate(inp):
        nbs = set()
        start = None
        cur_num = 0
        for x, char in enumerate(row):
            if char.isdigit():
                if not start:
                    start = (x, y)
                cur_num *= 10
                cur_num += int(char)
                nbs.update(get_gear_nbs(inp, x, y))
            else:
                for nb in nbs:
                    gear_to_nbs[nb].add((start, cur_num))
                start = None
                nbs = set()
                cur_num = 0
        # End of row
        for nb in nbs:
            gear_to_nbs[nb].add((start, cur_num))

    sum = 0
    for gear, nbs in gear_to_nbs.items():
        if len(nbs) == 2:
            lst = list(nbs)
            sum += lst[0][1] * lst[1][1]
    return sum


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
