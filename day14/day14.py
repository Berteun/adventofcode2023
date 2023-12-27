#!/usr/bin/env python3.12
# -*- coding: utf-8 -*-
import os.path
import sys

sys.path.insert(0, os.path.abspath(os.path.join(__file__, '..', '..')))
import aoc

def roll_up_once(inp):
    change = False
    for y in range(1, inp.maxy):
        for x in range(inp.maxx):
            if inp[x, y] == 'O' and inp[x, y - 1] == '.':
                inp[x, y] = '.'
                inp[x, y - 1] = 'O'
                change = True
    return change


def cycle_up(inp):
    change = True
    while change:
        change = roll_up_once(inp)
    return inp


def cycle_down(inp):
    change = True
    inp.flip()
    while change:
        change = roll_up_once(inp)
    inp.flip()
    return inp


def cycle_west(inp):
    inp.transpose()
    change = True
    while change:
        change = roll_up_once(inp)
    inp.transpose()
    return inp

def cycle_east(inp):
    inp.transpose()
    inp = cycle_down(inp)
    inp.transpose()
    return inp


def weight(inp):
    row_weight = len(inp)
    weight = 0
    for y in inp.rows():
        for p in inp.row(y):
            if inp[p] == 'O':
                weight += row_weight
        row_weight -= 1
    return weight


def part1(inp):
    inp = cycle_up(inp)
    return weight(inp)


def full_cycle(inp):
    inp = cycle_up(inp)
    inp = cycle_west(inp)
    inp = cycle_down(inp)
    return cycle_east(inp)


def part2(inp):
    steps = 0
    d = {}
    weights = []
    weights.append(weight(inp))
    while True:
        inp = full_cycle(inp)
        steps += 1
        weights.append(weight(inp))
        h = hash(''.join([''.join(r) for r in inp.grid]))
        if h in d:
            break
        else:
            d[h] = steps

    cycle_length = steps - d[h]
    offset = steps - cycle_length
    target = (1_000_000_000 - offset) % cycle_length
    return weights[offset + target]


def main(input_file):
    inp = aoc.read_grid(input_file)

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
