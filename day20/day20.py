#!/usr/bin/env python3.12
from dataclasses import dataclass
from collections import deque

# -*- coding: utf-8 -*-
import math
import os.path
import sys

sys.path.insert(0, os.path.abspath(os.path.join(__file__, '..', '..')))
import aoc


@dataclass
class Node:
    name: str
    kind: str
    outputs: list[str]
    state: bool
    inputs: dict

def parse_line(line):
    raw_source, raw_dests = line.split(' -> ')
    dests = raw_dests.split(', ')
    match raw_source[0]:
        case 'b':
            node =  Node(raw_source, 'bc', dests, False, {})
        case '%':
            node = Node(raw_source[1:], 'ff', dests, False, {})
        case '&':
            node = Node(raw_source[1:], 'inv', dests, False, {})
        case _:
            print(line)
            assert False
    return node.name, node



def read_input(input_file):
    d = dict(parse_line(ln)
            for ln in open(input_file).read().rstrip().split('\n'))
    for node in d:
        if d[node].kind == 'inv':
            for other in d.values():
                if node in other.outputs:
                    d[node].inputs[other.name] = None
    return d

def part1(nodes):
    high = 0
    low = 0
    done = False
    presses = 0
    cycles = {}
    for _ in range(10_000):
        queue = deque([('button', 'broadcaster', 'low')])
        while queue:
            src, dest, signal = queue.popleft()
            #print(f'{src} -{signal}-> {dest}')
            if signal == 'high':
                high += 1
            else:
                low += 1
            if dest == 'rx' and signal == 'low':
                done = True
            if dest not in nodes:
                continue
            d = nodes[dest]
            match d.kind:
                case 'bc':
                    for o in d.outputs:
                        queue.append((d.name, o, signal))
                case 'ff':
                    if signal == 'low':
                        d.state = not d.state
                        out = 'high' if d.state else 'low'
                        for o in d.outputs:
                            queue.append((d.name, o, out))
                case 'inv':
                    d.inputs[src] = signal
                    out = 'low' if all(v == 'high' for v in d.inputs.values()) else 'high'
                    for o in d.outputs:
                        queue.append((d.name, o, out))
    return high * low

def part2(nodes):
    high = 0
    low = 0
    done = False
    presses = 0
    cycles = {}
    while not done:
        queue = deque([('button', 'broadcaster', 'low')])
        presses += 1
        while queue:
            src, dest, signal = queue.popleft()
            #print(f'{src} -{signal}-> {dest}')
            if dest in ('nh', 'xm', 'dr', 'tr') and signal == 'low':
                cycles[dest] = presses
                if len(cycles) == 4:
                    return math.prod(cycles.values())
            if dest == 'rx' and signal == 'low':
                done = True
            if dest not in nodes:
                continue
            d = nodes[dest]
            match d.kind:
                case 'bc':
                    for o in d.outputs:
                        queue.append((d.name, o, signal))
                case 'ff':
                    if signal == 'low':
                        d.state = not d.state
                        out = 'high' if d.state else 'low'
                        for o in d.outputs:
                            queue.append((d.name, o, out))
                case 'inv':
                    d.inputs[src] = signal
                    out = 'low' if all(v == 'high' for v in d.inputs.values()) else 'high'
                    for o in d.outputs:
                        queue.append((d.name, o, out))
    return presses

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
