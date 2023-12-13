#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def parse_block(block):
    return block.split('\n')


def read_input(input_file):
    return [parse_block(ln)
            for ln in open(input_file).read().rstrip().split('\n\n')]


def transpose(block):
    tr = zip(*[list(b) for b in block])
    return [''.join(r) for r in tr]


def get_reflections(block):
    reflections = []
    for n in range(1, len(block)):
        is_reflect = True
        for y in range(n):
            if n + y >= len(block):
                break
            if block[n - y - 1] != block[n + y]:
                is_reflect = False
                break
        if is_reflect:
            reflections.append(n)
    return reflections

def get_smudge_reflections(block):
    reflections = []
    for n in range(1, len(block)):
        is_reflect = True
        is_smudge_reflect = False
        for y in range(n):
            above = n - y - 1
            below = n + y

            if below >= len(block):
                break
            if block[above] != block[below]:
                if is_smudge_reflect:
                    is_reflect = False
                    break
                else:
                    i_list = [i for i in range(len(block[above])) if block[above][i] != block[below][i]]
                    if len(i_list) == 1:
                        is_smudge_reflect = True
                    else:
                        is_reflect = False
                        break
        if is_reflect and is_smudge_reflect:
            reflections.append(n)
    return reflections


def part12(inp, get_ref):
    tot = 0
    for b in inp:
        v = get_ref(b)
        tot += sum(100*x for x in v)
        h = get_ref(transpose(b))
        tot += sum(h)
    return tot


def main(input_file):
    inp = read_input(input_file)

    print(part12(inp, get_reflections))
    print(part12(inp, get_smudge_reflections))


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'input'

    main(input_file)

# vim: sts=4:ts=4:et:sw=4:number:
