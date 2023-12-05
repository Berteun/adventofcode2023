#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import namedtuple

Map = namedtuple('Map', ['start', 'end', 'offset'])


def parse_map(block):
    lines = block.strip().split('\n')
    result = []
    for ln in lines[1:]:
        dst, src, rng = ln.split()
        result.append(Map(int(src), int(src) + int(rng), int(dst) - int(src)))
    return result


def read_input(input_file):
    blocks = open(input_file).read().rstrip().split('\n\n')
    seeds = [int(s) for s in blocks[0].split(':')[1].strip().split()]
    maps = [parse_map(blocks[b]) for b in range(1, len(blocks))]
    return seeds, maps


def map_seed(s, maps):
    for m in maps:
        for (start, end, offset) in m:
            if start <= s < end:
                s += offset
                break
    return s


def part1(seeds, maps):
    locs = [map_seed(s, maps) for s in seeds]
    return min(locs)


def split(start, end, rstart, rend):
    overlap = None
    non_overlap = []
    if rstart < start:
        non_overlap.append((rstart, min(rend, start)))
    if rend > end:
        non_overlap.append((max(rstart, end), rend))
    if start < rend and rstart < end:
        overlap = (max(start, rstart), min(rend, end))
    return overlap, non_overlap


def map_seed_ranges(s, maps):
    ranges = [s]
    for m in maps:
        new_ranges = []
        for (start, end, offset) in m:
            i = 0
            while i < len(ranges):
                if ranges[i] is None:
                    i += 1
                    continue
                (rstart, rend) = ranges[i]
                overlap, non_overlap = split(start, end, rstart, rend)
                if overlap is not None:
                    ranges[i] = None
                    ranges.extend(non_overlap)
                    new_ranges.append((overlap[0] + offset, overlap[1] + offset))
                i += 1
        ranges = list(set(new_ranges + [r for r in ranges if r is not None]))
    return ranges


def part2(seeds, maps):
    pairs = [(seeds[i], seeds[i] + seeds[i+1]) for i in range(0, len(seeds), 2)]
    mins = []
    for pair in pairs:
        ranges = map_seed_ranges(pair, maps)
        mins.append(min(ranges)[0])
    return min(mins)


def main(input_file):
    seeds, maps = read_input(input_file)
    print(part1(seeds, maps))
    print(part2(seeds, maps))


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'input'

    main(input_file)

# vim: sts=4:ts=4:et:sw=4:number:
