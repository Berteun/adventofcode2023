#!/usr/bin/env python3.12
# -*- coding: utf-8 -*-
from collections import deque, defaultdict

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


def neighbours(grid, start, target):
    result = defaultdict(set)
    cur = start
    stack = deque([(cur, 0, cur, [])])
    seen = set([cur])
    while stack:
        cur, steps, last_intersection, path = stack.popleft()
        nbs = grid.neighbours(cur, lambda c: c != '#')
        if len(nbs) > 2 or cur == target:
            seen.add((cur, cur))
            result[last_intersection].add((cur, steps))
            result[cur].add((last_intersection, steps))
            last_intersection = cur
            steps = 0
            path = []

        for n in nbs:
            key = (last_intersection, n)
            if key not in seen:
                seen.add(key)
                stack.append((n, steps + 1, last_intersection, path + [n]))

    return result


def print_grid(grid, seen):
    for r in grid.rows():
        for p in grid.row(r):
            if p in seen:
                sys.stdout.write(f'{aoc.fg.red}{grid[p]}{aoc.fg.reset}')
            else:
                sys.stdout.write(grid[p])
        sys.stdout.write('\n')


# Is this slow? Yes. Does it find the longest path after a while, yes. Just observe the output.
def part2(grid):
    start = find_start(grid)
    end = find_end(grid)
    nbs = neighbours(grid, start, end)
    max_steps = -1
    stack = [(start, 0, frozenset([start]))]
    while stack:
        cur, steps, path = stack.pop()
        if cur == end and steps > max_steps:
            max_steps = steps

        nb_set = nbs[cur]
        for (nb, next_steps) in nb_set:
            if nb in path:
                continue
            new_path = path.union([nb])
            new_state = (nb, steps + next_steps, new_path)
            stack.append(new_state)

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
