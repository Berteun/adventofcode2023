#!/usr/bin/env python3.12
# -*- coding: utf-8 -*-
import os.path
import sys
from functools import cache

sys.path.insert(0, os.path.abspath(os.path.join(__file__, '..', '..')))
import aoc

from collections import deque

def get_start(inp):
    for y in inp.rows():
        for p in inp.row(y):
            if inp[p] == 'S':
                return p
    assert False

MAX_STEPS = 64
def part1(inp, start):
    steps = 0
    queue = deque([(start, steps)])
    seen = set()
    while True:
        cur, steps = queue.popleft()
        if steps > MAX_STEPS:
            break
        for nb in inp.neighbours(cur, lambda c: c == '.'):
            key = (nb, steps + 1)
            if not key in seen:
                seen.add(key)
                queue.append(key)
    tot = 0
    for (n, steps) in seen:
        if steps == MAX_STEPS:
            tot += 1
    return tot


def neighbours(grid, offsets, point: aoc.Point):
    x, y = point.x, point.y
    nbs = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx = x + dx
        ny = y + dy
        x_off, y_off = offsets
        if nx < 0:
            x_off -= 1
            nx += grid.maxx
        elif nx >= grid.maxx:
            x_off += 1
            nx -= grid.maxx

        if ny < 0:
            y_off -= 1
            ny += grid.maxy
        elif ny >= grid.maxy:
            y_off += 1
            ny -= grid.maxy

        if grid.grid[ny][nx] == '.':
            nbs.append((aoc.Point(nx, ny), (x_off, y_off)))

    return nbs


#MAX_STEPS_2 = 26501365

def part2(inp, start, max_steps):
    steps = 0
    queue = deque([(start, (0, 0), steps)])
    seen = set()
    result = [0] * (max_steps + 1)
    d_result = [0] * (max_steps + 1) 
    dd_result = [0] * (max_steps + 1)
    cur_steps = -1
    while True:
        cur, offsets, steps = queue.popleft()
        if steps != cur_steps:
            if cur_steps >= inp.maxx:
                d_result[cur_steps] = result[cur_steps] - result[cur_steps - inp.maxx]
                dd_result[cur_steps] = d_result[cur_steps] - d_result[cur_steps - inp.maxx]
                slice = set(dd_result[cur_steps - inp.maxx + 1:cur_steps + 1])
                if len(slice) == 1:
                    break
            cur_steps = steps
        result[steps] += 1
        for nb, n_offsets in neighbours(inp, offsets, cur):
            key = (nb, n_offsets, steps + 1)
            if key not in seen:
                seen.add(key)
                queue.append(key)

    # Now extrapolate 
    dd = dd_result[cur_steps]
    while cur_steps <= max_steps:
        d_result[cur_steps] = d_result[cur_steps - inp.maxx] + dd
        result[cur_steps] = result[cur_steps - inp.maxx] + d_result[cur_steps]
        cur_steps += 1
        
    return result[max_steps]



def main(input_file):
    inp = aoc.read_grid(input_file)
    start = get_start(inp)
    inp[start] = '.'

    print(part1(inp, start))
    print(part2(inp, start, 26501365))


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'input'

    main(input_file)

# vim: sts=4:ts=4:et:sw=4:number:
