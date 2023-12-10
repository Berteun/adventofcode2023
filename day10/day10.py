#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys


class fg:
    black = "\u001b[30m"
    red = "\u001b[31m"
    green = "\u001b[32m"
    yellow = "\u001b[33m"
    blue = "\u001b[34m"
    magenta = "\u001b[35m"
    cyan = "\u001b[36m"
    white = "\u001b[37m"
    reset = "\u001b[0m"
    bold = "\u001b[1m"

PIPES = {
    '|': [ -1j, 1j],
    '-': [ -1 , 1 ],
    'L': [  1 ,-1j],
    'J': [ -1, -1j],
    '7': [ -1 , 1j],
    'F': [  1,  1j],
    '.': [],
}


TRANS = {
    '|': '║',
    'L': '╚',
    '-': '═',
    '7': '╗',
    'J': '╝',
    'F': '╔',
}

def read_input(input_file):
    return [list(ln) for ln in open(input_file).read().rstrip().split('\n')]


def get_start(inp):
    for y, row in enumerate(inp):
        for x, c in enumerate(row):
            if c == 'S':
                return (x, y)
    assert False


def to_p(c):
    return int(c.real), int(c.imag)

def fr_p(x, y):
    return x + y * 1j

def get_nbs(inp, c):
    x, y = to_p(c)
    if x < 0 or x >= len(inp[0]):
        return []
    if y < 0 or y >= len(inp):
        return []

    return [c + off for off in PIPES[inp[y][x]]]


def determine_start(inp, start):
    c = fr_p(*start)
    for pipe in PIPES:
        if pipe == '.':
            continue
        for offset in PIPES[pipe]:
            if c not in get_nbs(inp, c + offset):
                break
        else:
            return pipe


def walk_loop(inp, start):
    d = {}
    c = fr_p(*start)
    nbs = get_nbs(inp, c)
    prev = c
    cur = nbs[0]
    steps = 1
    on_loop = set([c])
    while cur != c:
        p = to_p(cur)
        on_loop.add(cur)
        nbs = get_nbs(inp, cur)
        nbs.remove(prev)
        prev = cur
        cur = nbs[0]
        steps += 1
    return steps, on_loop

def part1(inp):
    start = get_start(inp)
    start_kind = determine_start(inp, start)
    start_x, start_y = start
    inp[start_y][start_x] = start_kind
    steps, on_loop = walk_loop(inp, start)
    return steps//2, on_loop

def part2(inp, loop):
    in_loop = set()
    on_loop = set()
    out_loop = set()
    for y in range(len(inp)):
        for x in range(len(inp[y])):
            c = fr_p(x, y)
            if c in loop:
                on_loop.add(c)
                #print(f"({x},{y}) is on the loop")
                continue
            crosses = 0
            sx = x
            while sx >= 1:
                sx -= 1
                if inp[y][sx] in ('|', '7', 'F') and fr_p(sx, y) in loop:
                    crosses += 1
            if crosses % 2 == 0:
                out_loop.add(c)
            else:
                in_loop.add(c)

    # Print it
    for y in range(len(inp)):
        for x in range(len(inp[y])):
            c = fr_p(x, y)
            if c in out_loop:
                sys.stdout.write('O')
                continue
            if c in in_loop:
                sys.stdout.write(f'{fg.red}I{fg.reset}')
                continue
            sys.stdout.write(f"{fg.cyan}{TRANS[inp[y][x]]}{fg.reset}")
        sys.stdout.write('\n')

    return len(in_loop)


def main(input_file):
    inp = read_input(input_file)

    steps, on_loop = part1(inp)
    print(steps)

    print(part2(inp, on_loop))


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'input'

    main(input_file)

# vim: sts=4:ts=4:et:sw=4:number:
