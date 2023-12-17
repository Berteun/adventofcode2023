#!/usr/bin/env python3.12
# -*- coding: utf-8 -*-
import heapq
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

def parse_line(line):
    return list(int(i) for i in line)


def read_input(input_file):
    return [parse_line(ln)
            for ln in open(input_file).read().rstrip().split('\n')]


LT = (-1, 0)
RT = (1, 0)
UP = (0, -1)
DN = (0, 1)

DELTAS = (LT, RT, UP, DN)

def get_deltas(prev):
    if not prev:
        return DELTAS

    #print('prev', prev)
    p = prev[-1]
    if p == LT:
        deltas = (LT, UP, DN)
    elif p == UP:
        deltas = (LT, RT, UP)
    elif p == DN:
        deltas = (LT, DN, RT)
    elif p == RT:
        deltas = (RT, UP, DN)
    else:
        print(prev)
        assert False

    if len(prev) > 2 and prev[-1] == prev[-2] == prev[-3]:
        deltas = [d for d in deltas if d != prev[-1]]
    return deltas


def get_deltas2(prev):
    if not prev:
        deltas = DELTAS
    else:
        p = prev[-1]
        if p[0] < 0:  # Left
            deltas = (UP, DN)
        elif p[1] < 0:  # Up
            deltas = (LT, RT)
        elif p[1] > 0:  # Down
            deltas = (LT, RT)
        elif p[0] > 0:  # Right
            deltas = (UP, DN)
        else:
            print(prev)
            assert False

    new_deltas = []
    for d in deltas:
        for i in range(4, 11):
            new_deltas.append((d[0] * i, d[1] * i))
    return new_deltas


def neighbours(inp, node, prev):
    # print('nbs', node, prev)
    deltas = get_deltas(prev)
    nbs = []
    (x, y) = node
    for dir in deltas:
        dx, dy = dir
        nx = x + dx
        ny = y + dy
        if nx < 0 or ny < 0 or nx >= len(inp[0]) or ny >= len(inp):
            continue
        nbs.append(((nx, ny), inp[ny][nx], dir))
    return nbs


def neighbours2(inp, node, prev):
    # print('nbs', node, prev)
    deltas = get_deltas2(prev)
    nbs = []
    (x, y) = node
    for dir in deltas:
        dx, dy = dir
        nx = x + dx
        ny = y + dy
        if nx < 0 or ny < 0 or nx >= len(inp[0]) or ny >= len(inp):
            continue
        if dx != 0:
            cost = sum(inp[ny][cx] for cx in range(nx, x, -1 if dx > 0 else 1))
        else:
            cost = sum(inp[cy][nx] for cy in range(ny, y, -1 if dy > 0 else 1))
        #print(f'cost={cost} from {x},{y} to {nx},{ny}')
        nbs.append(((nx, ny), cost, dir))
    return nbs


def print_path(inp, prev, dest):
    path = set([dest[0]])
    print(prev)
    while dest in prev:
        path.add(prev[dest][0])
        dest = prev[dest]
    print('path', path)
    cost = 0
    for y, row in enumerate(inp):
        for x, c in enumerate(row):
            if (x, y) in path:
                sys.stdout.write(f"{fg.red}{c}{fg.reset}")
                if (x, y) != (0, 0):
                    cost += c
            else:
                sys.stdout.write(str(c))
        sys.stdout.write('\n')
    sys.stdout.write('\n')
    print('cost', cost)


def part1(inp):
    start = (0, 0)
    dest = (len(inp[0]) - 1, len(inp) - 1)
    pth = {}
    dist = {(start, tuple()): 0}
    Q = [(0, start, tuple())]

    while Q:
        loss, node, prev = heapq.heappop(Q)
        # print(loss, node, prev)
        key = (node, prev)
        if key in dist and loss > dist[key]:
            continue

        for new_node, cost, dir in neighbours(inp, node, prev):
            hist = tuple(prev[-2:] + (dir,))
            new_key = (new_node, hist)
            new_cost = dist[key] + cost

            if new_node == dest:
                pth[new_key] = key
                #print_path(inp, pth, new_key)
                return new_cost

            if new_key not in dist or new_cost < dist[new_key]:
                dist[new_key] = new_cost
                pth[new_key] = key
                # print('hist', hist)
                heapq.heappush(Q, (new_cost, new_node, hist))
    return -1


def part2(inp):
    start = (0, 0)
    dest = (len(inp[0]) - 1, len(inp) - 1)
    pth = {}
    dist = {(start, tuple()): 0}
    Q = [(0, start, tuple())]

    while Q:
        loss, node, prev = heapq.heappop(Q)
        key = (node, prev)
        if key in dist and loss > dist[key]:
            continue

        if node == dest:
            #print_path(inp, pth, key)
            return loss

        for new_node, cost, dir in neighbours2(inp, node, prev):
            hist = (dir,)
            new_key = (new_node, hist)
            new_cost = dist[key] + cost


            if new_key not in dist or new_cost < dist[new_key]:
                dist[new_key] = new_cost
                pth[new_key] = key
                #print('hist', hist)
                heapq.heappush(Q, (new_cost, new_node, hist))
    return -1


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
