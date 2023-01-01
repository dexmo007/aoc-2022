from dataclasses import dataclass
from functools import reduce
import re


with open('sample.txt') as f:
    lines = f.readlines()

pattern = re.compile(
    r'^Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)$')


@dataclass
class Sensor:
    sx: int
    sy: int
    bx: int
    by: int

    def shift(self, shift):
        x, y = shift
        self.sx -= x
        self.sy -= y
        self.bx -= x
        self.by -= y


def parse_sensor(line: str):
    m = pattern.match(line.strip())
    vals = [int(v) for v in m.groups()]
    return Sensor(*vals)


sensors = [parse_sensor(line) for line in lines if line.strip()]


def get_aggr(aggr, accessor):
    return reduce(lambda acc, cur: aggr(*accessor(cur)) if acc is None else aggr(acc, *accessor(cur)), sensors, None)


min_x = get_aggr(min, lambda s: (s.sx, s.bx))
max_x = get_aggr(max, lambda s: (s.sx, s.bx))
min_y = get_aggr(min, lambda s: (s.sy, s.by))
max_y = get_aggr(max, lambda s: (s.sy, s.by))

grid = [['.' for _ in range(max_x - min_x + 1)]
        for _ in range(max_y - min_y + 1)]

for sensor in sensors:
    sensor.shift((min_x, min_y))
    grid[sensor.sy][sensor.sx] = 'S'
    grid[sensor.by][sensor.bx] = 'B'

for row in grid:
    for cell in row:
        print(cell, end='')
    print()
