#!/usr/bin/env python
# -*- coding: utf-8 -*-

digits = {
    'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8,  'nine': 9
}

def get_digits(line):
    for c in line:
        if c.isdigit():
            first = c
            break

    for c in reversed(line):
        if c.isdigit():
            last = c
            break
    return int(first + last)

def helper(line):
    for i in range(len(line)):
        if line[i].isdigit():
            return line[i]
        for d in digits:
            if line[i:].startswith(d):
                return str(digits[d])

def rhelper(line):
    for i in range(len(line) - 1, -1, -1):
        if line[i].isdigit():
            return line[i]
        for d in digits:
            if line[i:].startswith(d):
                return str(digits[d])


def get_digits2(line):
    first = helper(line)
    last = rhelper(line) 

    return int(first + last)

def read_input():
    return [l for l in open('input').read().split('\n') if l]


def part1(lines):
    codes = [get_digits(l) for l in lines]
    return sum(codes)

def part2(lines):
    codes = [get_digits2(l) for l in lines]
    return sum(codes)

def main():
    inp = read_input()

    print(part1(inp))
    print(part2(inp))


if __name__ == '__main__':
    main()
