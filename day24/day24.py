#!/usr/bin/env python3.12
# -*- coding: utf-8 -*-
from fractions import Fraction
from dataclasses import dataclass

import os.path
import sys

sys.path.insert(0, os.path.abspath(os.path.join(__file__, '..', '..')))
import aoc
import z3

@dataclass(frozen=True)
class Stone:
    px: int
    py: int
    pz: int
    vx: int
    vy: int
    vz: int

    # x = px + vx = > t = (x - px)/vx
    # y = py + vy t
    # => y = py + vy(x - px)/vx
    # => y = vy/vx * (x - px) + py
    # => y = vy/vx x + py - (px*vy/vx)
    def get_rc(self):
        return Fraction(self.vy, self.vx)

    def get_off(self):
        return self.py - Fraction(self.px * self.vy, self.vx)

    def crosses2d(self, other):
        # Solve y = ax + c and y = bx + d
        # so ax + b = cx + d
        a = self.get_rc()
        c = self.get_off()

        b = other.get_rc()
        d = other.get_off()

        # Parallel
        if (a - b) == 0:
            return None

        x = Fraction(d - c, a - b)
        y = x * self.get_rc() + self.get_off()

        other_y = x * other.get_rc() + other.get_off()
        assert y == other_y, f"Fail {x} {y} {other_y}"

        t1 = (x - self.px)/self.vx
        t2 = (x - other.px)/other.vx

        # Only forward in time
        if t1 > 0 and t2 > 0:
            return x, y
        else:
            return None

def parse_line(line):
    raw_pos, raw_vel = line.split('@')
    px, py, pz = (int(n.strip()) for n in raw_pos.split(','))
    vx, vy, vz = (int(n.strip()) for n in raw_vel.split(','))
    return Stone(px, py, pz, vx, vy, vz)


def read_input(input_file):
    return [parse_line(ln)
            for ln in open(input_file).read().rstrip().split('\n')]


def part1(inp):
    tot = 0
    lb = 200000000000000
    ub = 400000000000000
    for i, stone in enumerate(inp):
        for other in inp[i+1:]:
            crosses = stone.crosses2d(other)
            if crosses is not None:
                (x, y) = crosses
                if lb <= x <= ub and lb <= y <= ub:
                    tot += 1
    return tot


def part2(inp):
    sx, sy, sz = z3.Int('sx'), z3.Int('sy'), z3.Int('sz')
    vx, vy, vz = z3.Int('vx'), z3.Int('vy'), z3.Int('vz')

    s = z3.Solver()

    MAX = 9
    t = [z3.Int(f't{i}') for i in range(MAX)]
    s.add(z3.Distinct(t))
    for i, stone in enumerate(inp[:MAX]):
        s.add(t[i] > 0)
        s.add(sx + t[i] * vx == stone.px + stone.vx * t[i])
        s.add(sy + t[i] * vy == stone.py + stone.vy * t[i])
        s.add(sz + t[i] * vz == stone.pz + stone.vz * t[i])

    print(s.check())
    m = s.model()
    print(f'sx={m[sx]}, sy={m[sy]}, sz={m[sz]}')
    print(f'vx={m[vx]}, vy={m[vy]}, vz={m[vz]}')

    return m.evaluate(sx + sy + sz)


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
