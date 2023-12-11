#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def read_input(input_file):
    return [list(ln) for ln in open(input_file).read().rstrip().split('\n')]


def empty_cols(inp):
    rows = []
    for y in range(len(inp)):
        if set(inp[y]) == set(['.']):
            rows.append(y)

    cols = []
    for x in range(len(inp[0])):
        col = [row[x] for row in inp]
        if set(col) == set(['.']):
            cols.append(x)

    return rows, cols


def expand(inp, rows, cols, expansion):
    base_coords = []
    for y, row in enumerate(inp):
        for x, c in enumerate(row):
            if c == '#':
                base_coords.append((x, y))

    coords = []
    for coord in base_coords:
        nc = [coord[0], coord[1]]
        for y in rows:
            if coord[1] > y:
                nc[1] += (expansion - 1)

        for x in cols:
            if coord[0] > x:
                nc[0] += (expansion - 1)
        coords.append(nc)

    return coords


def dist(coords):
    tot = 0
    for fr in range(len(coords)):
        for to in range(fr + 1, len(coords)):
            fc = coords[fr]
            tc = coords[to]
            dist = abs(fc[0] - tc[0]) + abs(fc[1] - tc[1])
            tot += dist
    return tot


def part1(inp):
    rows, cols = empty_cols(inp)
    return dist(expand(inp, rows, cols, 2))


def part2(inp):
    rows, cols = empty_cols(inp)
    return dist(expand(inp, rows, cols, 1000_000))


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
