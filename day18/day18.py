#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import deque

def parse_line(line):
    d, a, col = line.split()
    return d, int(a), col[2:-1]


def read_input(input_file):
    return [parse_line(ln)
            for ln in open(input_file).read().rstrip().split('\n')]


DIR = {
    'R': 1,
    'L': -1,
    'U': -1j,
    'D': 1j,
}

def boundaries(seen):
    minx = 1e10
    miny = 1e10
    maxx = -1
    maxy = -1

    for s in seen:
        x = s.real
        y = s.imag
        minx = min(x, minx)
        maxx = max(x, maxx)
        miny = min(y, miny)
        maxy = max(y, maxy)
    return int(minx), int(miny), int(maxx), int(maxy)

def flood_fill(seen, start):
    q = deque()
    q.append(start)
    while q:
        n = q.popleft()
        for d in DIR.values():
            nb = n + d
            if nb not in seen:
                seen.add(nb)
                q.append(nb)
    return seen


def print_grid(seen):
    minx, miny, maxx, maxy = boundaries(seen)
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            if x + 1j * y in seen:
                sys.stdout.write('#')
            else:
                sys.stdout.write('.')
        sys.stdout.write('\n')
    sys.stdout.write('\n')

def part1(inp):
    seen = set()
    pos = 0 + 0j
    seen.add(pos)
    for (dir, a, _) in inp:
        for n in range(a):
            pos += DIR[dir]
            seen.add(pos)
    #print_grid(seen)
    flood_fill(seen, -1 + -1j)
    #print_grid(seen)

    return len(seen)

def shoelace(coord):
    l = len(coord)
    p = [(coord[i].real * coord[(i + 1) % l].imag) - (coord[i].real * coord[(i - 1) % l].imag) for i in range(l)]
    return abs(sum(p) / 2)

def decode(hex):
    dirs = ['R', 'D', 'L', 'U']
    n = ''.join(hex[:5])
    return int(n, 16), dirs[int(hex[-1])]

def part2(inp):
    coords = []
    pos = 0 + 0j
    coords.append(pos)
    bound = 0
    for _, _, hex in inp:
        a, dir = decode(hex)
        bound += a
        pos += DIR[dir] * a
        coords.append(pos)
    sl = shoelace(coords)
    return int((bound // 2) + sl + 1)


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
