import dataclasses


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


def read_input(input_file, line_parser=lambda ln: ln):
    with open(input_file, 'r') as f:
        return [line_parser(ln) for ln in f.read().rstrip().split('\n')]


@dataclasses.dataclass(eq=True, frozen=True, order=True)
class Point:
    x: int
    y: int

    def __add__(self, other: 'Point'):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Point'):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Point(self.x * scalar, self.y * scalar)


class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.maxx = len(grid[0])
        self.maxy = len(grid)

    def __getitem__(self, coordinate):
        if isinstance(coordinate, Point):
            return self.grid[coordinate.y][coordinate.x]
        if isinstance(coordinate, tuple):
            x, y = coordinate
            return self.grid[y][x]

    def __setitem__(self, coordinate, val):
        if isinstance(coordinate, Point):
            self.grid[coordinate.y][coordinate.x] = val
        if isinstance(coordinate, tuple):
            x, y = coordinate
            self.grid[y][x] = val

    def __len__(self):
        return len(self.grid)

    def rows(self, offset=0):
        return range(offset, self.maxy)

    def row(self, row: int):
        for x in range(self.maxx):
            yield Point(x, row)

    def transpose(self):
        self.grid = [list(r) for r in zip(*self.grid)]

    def flip(self):
        self.grid.reverse()

    def neighbours(self, point: Point, filter=lambda c: True):
        x, y = point.x, point.y
        nbs = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < self.maxx and 0 <= ny < self.maxy:
                if filter(self.grid[ny][nx]):
                    nbs.append(Point(nx, ny))
        return nbs

    def __str__(self):
        return '\n'.join([''.join(r) for r in self.grid])


def read_grid(input_file):
    return Grid(read_input(input_file, lambda ln: list(ln)))


def read_int_grid(input_file):
    return Grid(read_input(input_file, lambda ln: [int(n) for n in list(ln)]))
