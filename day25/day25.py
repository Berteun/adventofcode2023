#!/usr/bin/env python3.12
# -*- coding: utf-8 -*-
from collections import defaultdict, deque


def parse_line(line):
    source, dest = line.split(': ')
    return source, dest.split(' ')


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


def main(input_file):
    # Make dot file, look at it with eyes
    #convert_input(input_file)

    # Found:
    # 'fvh' - 'fch'
    # 'nvg' - 'vfj'
    # 'sqh' - 'jbz'

    G = read_input(input_file)

    G['fvh'].remove('fch')
    G['nvg'].remove('vfj')
    G['sqh'].remove('jbz')

    G['fch'].remove('fvh')
    G['vfj'].remove('nvg')
    G['jbz'].remove('sqh')

    q = deque(['fvh'])
    seen = set(['fvh'])
    while q:
        cur = q.popleft()
        for nb in G[cur]:
            if nb not in seen:
                seen.add(nb)
                q.append(nb)

    print(len(seen) * (len(G) - len(seen)))

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'input'

    main(input_file)

# vim: sts=4:ts=4:et:sw=4:number:
