#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def parse_line(line):
    return line


def read_input(input_file):
    if input_file == 'test':
        return ((7, 9), (15, 40), (30, 200))
    else:
        return ((51, 222), (92, 2031), (68, 1126), (90, 1225))


def read_input2(input_file):
    if input_file == 'test':
        return (71530, 940200)
    else:
        return (51926890, 222203111261225)


def part1(inp):
    all_ways = []
    for (time, rec) in inp:
        ways = 0
        for hold in range(time + 1):
            speed = hold
            dist = speed * (time - hold)
            if dist > rec:
                ways += 1
        all_ways.append(ways)
    prod = 1
    for w in all_ways:
        prod *= w
    return prod


def part2(inp):
    low_bound = 0
    time, rec = inp

    low_bound = 0
    for hold in range(time + 1):
        speed = hold
        dist = speed * (time - hold)
        if dist > rec:
            low_bound = hold
            break

    up_bound = 0
    for hold in range(time, -1, -1):
        speed = hold
        dist = speed * (time - hold)
        if dist > rec:
            up_bound = hold
            break

    return (up_bound + 1 - low_bound)


def main(input_file):
    inp1 = read_input(input_file)

    print(part1(inp1))

    inp2 = read_input2(input_file)
    print(part2(inp2))


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'input'

    main(input_file)

# vim: sts=4:ts=4:et:sw=4:number:
