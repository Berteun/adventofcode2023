#!/usr/bin/env python
# -*- coding: utf-8 -*-

def parse(l):
    game, rest = l.split(':')
    game_no = int(game.split(' ')[1])
    
    results = []
    for showing in rest.split(';'):
        result = { 'red' : 0, 'green': 0, 'blue': 0 }
        for no_color in showing.split(','):
            no, color = no_color.strip().split(' ')
            result[color] = int(no)
        results.append(result)
    return game_no, results
        
    
def is_possible(result):
    for showing in result:
        if showing['red'] > 12 or showing['green'] > 13 or showing['blue'] > 14:
            return False
    return True

def read_input():
    result = {}
    for l in open('input').read().split('\n'):
        if l.strip():
            id, showings = parse(l)
            result[id] = showings
    return result


def part1(input):
    sum = 0
    for game_id in input:
        if is_possible(input[game_id]):
            sum += game_id
    return sum

def get_min_cubes(result):
    r, g, b = 0, 0, 0 
    for showing in result:
        r = max(r, showing['red'])
        g = max(g, showing['green'])
        b = max(b, showing['blue'])
    return { 'red' : r, 'green': g, 'blue': b}

def power(cubes):
    return cubes['red'] * cubes['green'] * cubes['blue']

def part2(input):
    sum = 0
    for game_id in input:
        min_cubes = get_min_cubes(input[game_id])
        sum += power(min_cubes)
    return sum

def main():
    inp = read_input()

    print(part1(inp))
    print(part2(inp))


if __name__ == '__main__':
    main()
