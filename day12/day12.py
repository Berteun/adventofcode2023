#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from functools import cache
def parse_line(line):
    pat, gears = line.split(' ')
    return pat, [int(i) for i in gears.split(',')]


def read_input(input_file):
    return [parse_line(ln)
            for ln in open(input_file).read().rstrip().split('\n')]


def solve(pattern, gear_list):
    @cache
    def helper(pattern_pos, gears_pos, in_seq):
        if pattern_pos == len(pattern):
            return len(gear_list) == gears_pos

        result = 0
        if pattern[pattern_pos] != '.':
            # Append gear to pattern
            result += helper(pattern_pos + 1, gears_pos, in_seq + 1)
        if pattern[pattern_pos] != '#':
            # Finish a gear
            if gears_pos < len(gear_list) and in_seq == gear_list[gears_pos]:
                result += helper(pattern_pos + 1, gears_pos + 1, 0)
            # Simple '.', move forward
            elif in_seq == 0:
                result += helper(pattern_pos + 1, gears_pos, 0)

        return result
    return helper(0, 0, 0)


def part12(inp, rep=1):
    return sum(solve('?'.join([p] * rep) + '.', g * rep) for p, g in inp)


def main(input_file):
    inp = read_input(input_file)

    print(part12(inp, 1))
    print(part12(inp, 5))


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'input'

    main(input_file)

# vim: sts=4:ts=4:et:sw=4:number:
