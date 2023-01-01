from dataclasses import dataclass
import re
import os

with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as f:
    lines = f.readlines()

pattern = re.compile(
    r'^Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)$')


def manhattan_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


@dataclass
class Sensor:
    sx: int
    sy: int
    bx: int
    by: int

    @property
    def b(self):
        return self.bx, self.by

    @property
    def s(self):
        return self.sx, self.sy


def parse_sensor(line: str):
    m = pattern.match(line.strip())
    vals = [int(v) for v in m.groups()]
    return Sensor(*vals)


sensors = [parse_sensor(line) for line in lines if line.strip()]

query_y = 2000000
no_beacon_locations = set()

for sensor in sensors:
    d = manhattan_distance(sensor.s, sensor.b)
    # sensor does not concern queried row
    if query_y > sensor.sy + d or query_y < sensor.sy - d:
        continue

    dx = d - abs(query_y - sensor.sy)
    for xi in range(dx + 1):
        if sensor.b != (sensor.sx + xi, query_y):
            no_beacon_locations.add((sensor.sx + xi, query_y))
        if sensor.b != (sensor.sx - xi, query_y):
            no_beacon_locations.add((sensor.sx - xi, query_y))

print(len(no_beacon_locations))
