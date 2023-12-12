#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def parse_line(line):
    pat, gears = line.split(' ')
    gears = [int(i) for i in gears.split(',')]
    return pat, gears

def read_input(input_file):
    return [parse_line(ln)
            for ln in open(input_file).read().rstrip().split('\n')]


def generate_pos(pattern):
    if len(pattern) > 1:
        pos = generate_pos(pattern[1:])
    else:
        if pattern[0] == '?':
            return ['.', '#']
        else:
            return [pattern]

    result = []
    if pattern[0] == '?':
        for p in pos:
            result.append('.' + p)
            result.append('#' + p)
    else:
        for p in pos:
            result.append(pattern[0] + p)
    return result

def generate_pos(pattern):
    if len(pattern) > 1:
        pos = generate_pos(pattern[1:])
    else:
        if pattern[0] == '?':
            return ['.', '#']
        else:
            return [pattern]

    result = []
    if pattern[0] == '?':
        for p in pos:
            result.append('.' + p)
            result.append('#' + p)
    else:
        for p in pos:
            result.append(pattern[0] + p)
    return result

def count_gears(pattern):
    cur = 0
    r = []
    for g in pattern:
        if g == '#':
            cur += 1
        if g == '.':
            if cur > 0:
                r.append(cur)
                cur = 0
    if cur > 0:
        r.append(cur)
    return r

def part1(inp):
    tot = 0
    for (pat, gears) in inp:
        count = 0
        print(pat)
        for pos in generate_pos(pat):
            cg = count_gears(pos)
            if cg == gears:
                count += 1
        tot += count
    return tot


cache = {}
def solve(pattern, gear_list, pattern_pos, gears_in_seq, gears_pos):
    key = (pattern_pos, gears_in_seq, gears_pos)
    if key in cache:
        return cache[key]

    if pattern_pos == len(pattern):
        return int(len(gear_list) == gears_pos)

    if gears_pos == len(gear_list):
        if gears_in_seq > 0 or pattern[pattern_pos] == '#':
            return 0

    if pattern[pattern_pos] == '#':
        result = solve(pattern, gear_list, pattern_pos + 1, gears_in_seq + 1, gears_pos)

    elif gears_pos == len(gear_list) or pattern[pattern_pos] == '.':
        # Finish a gear
        if gears_pos < len(gear_list) and gears_in_seq == gear_list[gears_pos]:
            result = solve(pattern, gear_list, pattern_pos + 1, 0, gears_pos + 1)
        # Simple '.', move forward
        elif gears_in_seq == 0:
            result = solve(pattern, gear_list, pattern_pos + 1, 0, gears_pos)
        # Finishing a gear, but too long for pattern
        else:
            result = 0
    else:
        # Assume a '#'
        result = solve(pattern, gear_list, pattern_pos + 1, gears_in_seq + 1, gears_pos)

        # Inline the '.' case
        if gears_in_seq == gear_list[gears_pos]:
            result += solve(pattern, gear_list, pattern_pos + 1, 0, gears_pos + 1)
        elif gears_in_seq == 0:
            result += solve(pattern, gear_list, pattern_pos + 1, 0, gears_pos)
    cache[key] = result
    return result


def unfold(pat, gears):
    return '?'.join([pat] * 5) + '.', gears * 5


def part2(inp):
    global cache
    tot = 0
    for (pat, gears) in inp:
        upat, ugears = unfold(pat, gears)
        cache = {}
        count = solve(upat, ugears, 0, 0, 0)
        #print(upat, ugears, count)
        tot += count
    return tot


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
