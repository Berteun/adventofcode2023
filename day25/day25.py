#!/usr/bin/env python3.12
from collections import defaultdict, deque, Counter

# -*- coding: utf-8 -*-
import math
import os.path
import random
import sys

sys.path.insert(0, os.path.abspath(os.path.join(__file__, '..', '..')))
import aoc


# Use neato
def convert_input(input_file):
    print('graph day25 {')
    for ln in open(input_file).read().rstrip().split('\n'):
        n, nbs = parse_line(ln)
        for nb in nbs:
            print(f'    {n} -- {nb};')
    print('}')

def parse_line(line):
    source, dest = line.split(': ')
    return source, dest.split(' ')


def read_input(input_file):
    G = defaultdict(set)
    for ln in open(input_file).read().rstrip().split('\n'):
        n, nbs = parse_line(ln)
        G[n].update(nbs)
        for nb in nbs:
            G[nb].add(n)
    return G


def bfs(G, source):
    q = deque([source])
    seen = set(source)
    counts = Counter()
    while q:
        cur = q.popleft()
        for nb in G[cur]:
            if nb not in seen:
                seen.add(nb)
                q.append(nb)
                e = (cur, nb) if cur < nb else (nb, cur)
                counts[e] += 1
    return counts


def part1(G):

    counts = Counter()
    for source in G:
        counts.update(bfs(G, source))

    remove = counts.most_common(3)
    for ((source, target), _) in remove:
        G[source].remove(target)
        G[target].remove(source)

    q = deque([source])
    seen = set([source])
    while q:
        cur = q.popleft()
        for nb in G[cur]:
            if nb not in seen:
                seen.add(nb)
                q.append(nb)

    return len(seen) * (len(G) - len(seen))


def main(input_file):
    #convert_input(input_file)

    G = read_input(input_file)
    print(part1(G))


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'input'

    main(input_file)

# vim: sts=4:ts=4:et:sw=4:number:
