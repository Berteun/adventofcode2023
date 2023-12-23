#!/usr/bin/env python3.12
# -*- coding: utf-8 -*-
from collections import deque

import os.path
import sys

sys.path.insert(0, os.path.abspath(os.path.join(__file__, '..', '..')))
import aoc


def get_move(nb, cur):
    if nb.x != cur.x:
        return '<' if nb.x < cur.x else '>'
    return '^' if nb.y < cur.y else 'v'

def part1(grid):
    start = find_start(grid)
    end = find_end(grid)
    max_steps = -1
    longest_path = None

    stack = [(start, 0, frozenset())]
    while stack:
        cur, steps, path = stack.pop()

        if cur == end and steps > max_steps:
            max_steps = steps
            longest_path = path

        for nb in grid.neighbours(cur, lambda c: c != '#'):
            if nb not in path and (grid[nb] == '.' or grid[nb] == get_move(nb, cur)):
                new_state = (nb, steps + 1, path.union(frozenset([cur])))
                stack.append(new_state)

    if False: # Print path
        for r in grid.rows():
            for p in grid.row(r):
                if p in longest_path:
                    sys.stdout.write(f'{aoc.fg.red}{grid[p]}{aoc.fg.reset}')
                else:
                    sys.stdout.write(grid[p])
            sys.stdout.write('\n')

    return max_steps

# Is this slow? Yes. Does it find the longest path after a while, yes. Just observe the output.
def part2(grid):
    start = find_start(grid)
    end = find_end(grid)
    max_steps = -1
    longest_path = None

    stack = [(start, 0, None, frozenset())]
    while stack:
        cur, steps, prev, path = stack.pop()

        if cur == end and steps > max_steps:
            max_steps = steps
            longest_path = path
            print('>', max_steps)

        nbs = grid.neighbours(cur, lambda c: c != '#')
        if len(nbs) > 2:
            # Intersection
            path = path.union(frozenset([cur]))
        else:
            path = path

        for nb in grid.neighbours(cur, lambda c: c != '#'):
            if nb != prev and nb not in path:
                new_state = (nb, steps + 1, cur, path)
                stack.append(new_state)

    if False: # Print intersections
        for r in grid.rows():
            for p in grid.row(r):
                if p in longest_path:
                    sys.stdout.write(f'{aoc.fg.red}{grid[p]}{aoc.fg.reset}')
                else:
                    sys.stdout.write(grid[p])
            sys.stdout.write('\n')

    return max_steps

def find_start(grid):
    for p in grid.row(0):
        if grid[p] == '.':
            return p
    assert False


def find_end(grid):
    for p in grid.row(grid.maxy - 1):
        if grid[p] == '.':
            return p
    assert False


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
