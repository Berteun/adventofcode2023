#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def parse_line(line):
    return line


def read_input(input_file):
    return [list(ln)
            for ln in open(input_file).read().rstrip().split('\n')]


def roll_up_once(inp):
    change = False
    for y in range(1, len(inp)):
        for x in range(len(inp[y])):
            if inp[y][x] == 'O' and inp[y - 1][x] == '.':
                inp[y][x] = '.'
                inp[y - 1][x] = 'O'
                change = True
    return change


def cycle_up(inp):
    change = True
    while change:
        change = roll_up_once(inp)
    return inp


def cycle_down(inp):
    change = True
    inp = inp[::-1]
    while change:
        change = roll_up_once(inp)
    inp = inp[::-1]
    return inp


def cycle_west(inp):
    inp = transpose(inp)
    change = True
    while change:
        change = roll_up_once(inp)
    return transpose(inp)


def cycle_east(inp):
    inp = transpose(inp)
    inp = cycle_down(inp)
    return transpose(inp)


def transpose(inp):
    tr = [list(l) for l in zip(*inp)]
    return tr


def weight(inp):
    row_weight = len(inp)
    weight = 0
    for y in range(0, len(inp)):
        for x in range(len(inp[y])):
            if inp[y][x] == 'O':
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
        h = hash(''.join([''.join(r) for r in inp]))
        if h in d:
            break
        else:
            d[h] = steps

    cycle_length = steps - d[h]
    offset = steps - cycle_length
    target = (1_000_000_000 - offset) % cycle_length
    return weights[offset + target]


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
