#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

UP = (0 - 1j)
DN = (0 + 1j)
LT = (-1 + 0j)
RT = (1 + 0j)


def c2p(c):
    return (int(c.real), int(c.imag))


def p2c(x, y):
    return 1*x + 1j * y


def parse_line(line):
    return list(line)


def read_input(input_file):
    return [parse_line(ln)
            for ln in open(input_file).read().rstrip().split('\n')]


def printb(inp, energized):
    for y, r in enumerate(inp):
        for x, c in enumerate(r):
            if (x, y) in energized:
                sys.stdout.write('#')
            else:
                sys.stdout.write(c)
        sys.stdout.write('\n')
    sys.stdout.write('\n')


def get_energized(inp, start, dir):
    beams = [(start, dir)]
    seen = set()
    energized = set()
    while beams:
        c, dir = beams.pop()
        if (c, dir) in seen:
            continue
        seen.add((c, dir))
        (x, y) = c2p(c)
        if x < 0 or y < 0 or y >= len(inp) or x >= len(inp[0]):
            # Out of bounds
            continue
        energized.add((x, y))
        if (inp[y][x] == '.' or (inp[y][x] == '|' and dir in (UP, DN))
                or (inp[y][x] == '-' and dir in (LT, RT))):
            beams.append((c + dir, dir))
        elif inp[y][x] == '|' and (dir in (LT, RT)):
            beams.append((c + UP, UP))
            beams.append((c + DN, DN))
        elif inp[y][x] == '-' and (dir in (UP, DN)):
            beams.append((c + LT, LT))
            beams.append((c + RT, RT))
        elif inp[y][x] == '/' and dir == RT:
            beams.append((c + UP, UP))
        elif inp[y][x] == '/' and dir == LT:
            beams.append((c + DN, DN))
        elif inp[y][x] == '/' and dir == UP:
            beams.append((c + RT, RT))
        elif inp[y][x] == '/' and dir == DN:
            beams.append((c + LT, LT))
        elif inp[y][x] == '\\' and dir == RT:
            beams.append((c + DN, DN))
        elif inp[y][x] == '\\' and dir == LT:
            beams.append((c + UP, UP))
        elif inp[y][x] == '\\' and dir == UP:
            beams.append((c + LT, LT))
        elif inp[y][x] == '\\' and dir == DN:
            beams.append((c + RT, RT))
        else:
            print(inp[y][x], c, dir)
            assert False
    return len(energized)


def part1(inp):
    start = p2c(0, 0)
    dir = RT
    return get_energized(inp, start, dir)


def part2(inp):
    maxx = len(inp[0]) - 1
    maxy = len(inp) - 1
    minx = 0
    miny = 0

    max_e = 0
    for x in range(0, maxx + 1):
        max_e = max(max_e, get_energized(inp, p2c(x, miny), DN))
        max_e = max(max_e, get_energized(inp, p2c(x, maxy), UP))

    for y in range(0, maxy + 1):
        max_e = max(max_e, get_energized(inp, p2c(minx, y), RT))
        max_e = max(max_e, get_energized(inp, p2c(maxx, y), LT))

    return max_e


def main(input_file):
    inp = read_input(input_file)

    print(part1(inp))
    print(part2(inp))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'input'

    main(input_file)

# vim: sts=4:ts=4:et:sw=4:number:
