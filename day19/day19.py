#!/usr/bin/env python3.12
# -*- coding: utf-8 -*-
import math
import sys
import operator


class Rule:
    def __init__(self, raw_rule):
        if ':' in raw_rule:
            rule, dest = raw_rule.split(':')
            self.field = rule[0]
            self.op = operator.lt if rule[1] == '<' else operator.gt
            self.bound = int(rule[2:])
            self.desc = "{field}{rule[1]}{cmp}"
            self.dest = dest
        else:
            self.op = None
            self.dest = raw_rule

    def eval(self, item):
        if self.op:
            return self.op(item[self.field], self.bound)
        else:
            return True

    def __str__(self):
        if self.op:
            return "{self.field}{'>' if self.op == operator.gt else '<'}{self.bound}"
        else:
            return "T"


def parse_flow(line):
    name, remainder = line.split('{')
    rules = [Rule(cond) for cond in remainder[:-1].split(',')]
    return (name, rules)


def parse_item(raw_item):
    d = {}
    fields = raw_item[1:-1].split(',')
    for f in fields:
        key, value = f.split('=')
        d[key] = int(value)
    return d


def read_input(input_file):
    raw_flow, raw_items = open(input_file).read().rstrip().split('\n\n')
    flows = dict(parse_flow(f) for f in raw_flow.split('\n'))
    items = [parse_item(f) for f in raw_items.split('\n')]
    return flows, items


def accepted(item, flows):
    cur = 'in'
    while cur not in ('A', 'R'):
        for t in flows[cur]:
            if t.eval(item):
                cur = t.dest
                break
    return cur == 'A'


def part1(flows, items):
    tot = 0
    for item in items:
        if accepted(item, flows):
            s = sum(item.values())
            tot += s
    return tot


def branch(holds, cond, ranges):
    res = []

    for rng in ranges:
        new_range = rng.copy()
        lower, upper = rng[cond.field]

        if (cond.op == operator.gt) == holds:
            lower = max(lower, cond.bound + holds)
        else:
            upper = min(upper, cond.bound - holds)

        if lower <= upper:
            new_range[cond.field] = (lower, upper)
            res.append(new_range)
    return res


def accepting(state, flow_idx, flows):
    if state == 'R':
        return []
    if state == 'A':
        return [{
            'x': (1, 4000),
            'm': (1, 4000),
            'a': (1, 4000),
            's': (1, 4000),
        }]

    cond = flows[state][flow_idx]
    if cond.op is None:
        return accepting(cond.dest, 0, flows)

    return (branch(True, cond, accepting(cond.dest, 0, flows))
            + branch(False, cond, accepting(state, flow_idx + 1, flows)))


def part2(flows, items):
    def prod_range(r):
        return math.prod(1 + upper - lower for (lower, upper) in r.values())

    return sum(prod_range(r) for r in accepting('in', 0, flows))


def main(input_file):
    flows, items = read_input(input_file)

    print(part1(flows, items))
    print(part2(flows, items))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'input'

    main(input_file)

# vim: sts=4:ts=4:et:sw=4:number:
