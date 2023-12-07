#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
from collections import namedtuple, Counter

Card = namedtuple('Card', ['type_', 'hand', 'bid'])

FIVE = 7
FOUR = 6
FULL = 5
THRE = 4
TWOP = 3
ONEP = 2
HIGH = 1

def get_type(hand):
    counts = sorted(list(Counter(hand).values()))
    if counts == [5]:
        return FIVE
    if counts == [1, 4]:
        return FOUR
    if counts == [2, 3]:
        return FULL
    if counts == [1, 1, 3]:
        return THRE
    if counts == [1, 2, 2]:
        return TWOP
    if counts == [1, 1, 1, 2]:
        return ONEP
    if counts == [1, 1, 1, 1, 1]:
        return HIGH
    assert False


def get_type2(hand):
    c = Counter(hand)
    jokers = c['J']
    if (jokers == 0 or jokers == 5):
        return get_type(hand)

    del c['J']
    (crd, cnt) = c.most_common(1)[0]
    c[crd] += jokers

    return get_type(c.elements())


def parse_cards(cards, JACK=11):
    result = []
    for c in cards:
        if c.isdigit():
            result.append(int(c))
        else:
            result.append({
                'T': 10,
                'J': JACK,
                'Q': 12,
                'K': 13,
                'A': 14,
            }[c])
    return tuple(result)

def parse_line(line):
    cards, bid = line.split(' ')
    return Card(get_type(tuple(cards)), parse_cards(cards), int(bid))


def parse_line2(line):
    cards, bid = line.split(' ')
    return Card(get_type2(tuple(cards)), parse_cards(cards, JACK=1), int(bid))


def read_input(input_file, parser):
    return sorted(parser(ln) for ln in open(input_file).read().rstrip().split('\n'))


def part12(inp):
    return sum((i + 1) * t.bid for (i, t) in enumerate(inp))


def main(input_file):
    inp1 = read_input(input_file, parse_line)
    print(part12(inp1))

    inp2 = read_input(input_file, parse_line2)
    print(part12(inp2))


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'input'

    main(input_file)

# vim: sts=4:ts=4:et:sw=4:number:
