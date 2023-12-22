#!/usr/bin/env python3.12
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from collections import defaultdict

import os.path
import sys

sys.path.insert(0, os.path.abspath(os.path.join(__file__, '..', '..')))
import aoc


def minmax(x, y):
    return min(x, y), max(x, y)

@dataclass(frozen=True, eq=True)
class Coordinate:
    x: int
    y: int
    z: int

    def is_lower(self, other):
        return self.z < other.z

    def is_higher(self, other):
        return self.z > other.z

@dataclass(frozen=True, eq=True)
class Block:
    c1: Coordinate
    c2: Coordinate

    def get_points(self):
        c1, c2 = self.c1, self.c2
        x1, x2 = minmax(c1.x, c2.x)
        y1, y2 = minmax(c1.y, c2.y)
        z1, z2 = minmax(c1.z, c2.z)

        res = []
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    res.append(Coordinate(x, y, z))
        return res

    def move_down(self):
        return Block(
            Coordinate(self.c1.x, self.c1.y, self.c1.z - 1),
            Coordinate(self.c2.x, self.c2.y, self.c2.z - 1)
        )

    def get_points_below(self):
        c1, c2 = self.c1, self.c2
        x1, x2 = minmax(c1.x, c2.x)
        y1, y2 = minmax(c1.y, c2.y)
        z = min(c1.z, c2.z)

        res = set()
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                res.add(Coordinate(x, y, z - 1))
        return res

    def get_points_above(self):
        c1, c2 = self.c1, self.c2
        x1, x2 = minmax(c1.x, c2.x)
        y1, y2 = minmax(c1.y, c2.y)
        z = max(c1.z, c2.z)

        res = set()
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                res.add(Coordinate(x, y, z + 1))
        return res

    def at_bottom(self):
        return self.c1.z == 1

def parse_line(line):
    raw_c1, raw_c2 = line.split('~')
    t1 = tuple(int(i) for i in raw_c1.split(','))
    t2 = tuple(int(i) for i in raw_c2.split(','))

    c1 = Coordinate(*t1)
    c2 = Coordinate(*t2)

    if c1.is_lower(c2):
        return Block(c1, c2)
    else:
        return Block(c2, c1)


def read_input(input_file):
    coordinates = [parse_line(ln)
            for ln in open(input_file).read().rstrip().split('\n')]
    coordinates.sort(key=lambda b: (b.c1.z, b.c1.y, b.c1.x))
    return coordinates

def stabilize(inp):
    stable = False
    blocks_moved = set()
    inp.sort(key=lambda b: b.c1.z)
    while not stable:
        stable = True
        blocked = set()
        for i in range(len(inp)):
            block = inp[i]
            if block.at_bottom():
                blocked.update(block.get_points())
                continue
            below = block.get_points_below()
            if below & blocked:
                blocked.update(block.get_points())
                continue

            blocks_moved.add(i)
            new_block = block.move_down()
            stable = False
            blocked.update(new_block.get_points())
            inp[i] = new_block
    return blocks_moved


def part1(inp):
    stabilize(inp)

    coordinate_block = dict()
    for i in range(len(inp)):
        block = inp[i]
        for c in block.get_points():
            coordinate_block[c] = i

    can_disintegrate = 0
    for i in range(len(inp)):
        block = inp[i]
        resting = set()
        for c in block.get_points_above():
            if c in coordinate_block:
                resting.add(coordinate_block[c])
        if not resting:
            can_disintegrate += 1
            continue

        can_destroy = True
        for r in resting:
            resting_block = inp[r]
            support = set()
            for c in resting_block.get_points_below():
                if c in coordinate_block:
                    support.add(coordinate_block[c])

            if len(support) == 1:
                can_destroy = False
                break

        if can_destroy:
            can_disintegrate += 1

    return can_disintegrate
                
def part2(inp):
    # First stabilize
    stabilize(inp)
    total_fall = 0
    for i in range(len(inp)):
        new_inp = inp[:i] + inp[i + 1:]
        fall = stabilize(new_inp)
        print(i)
        total_fall += len(fall)

    return total_fall

def main(input_file):
    inp = read_input(input_file)
    print(part1(inp))

    inp = read_input(input_file)
    print(part2(inp))


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'input'

    main(input_file)

# vim: sts=4:ts=4:et:sw=4:number:
