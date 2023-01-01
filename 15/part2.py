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


def ranges_diff(ranges, diff):
    new_ranges = []
    xd, yd = diff
    stopped_before = None
    for i, r in enumerate(ranges):
        x, y = r
        if xd > y:
            new_ranges.append(r)
            continue
        if yd < x:
            stopped_before = i
            break
        if x <= xd - 1:
            new_ranges.append((x, xd - 1))
        if y >= yd + 1:
            new_ranges.append((yd + 1, y))
    if stopped_before is not None:
        new_ranges += ranges[stopped_before:]
    return new_ranges


@dataclass
class Sensor:
    sx: int
    sy: int
    bx: int
    by: int
    d: int

    @property
    def b(self):
        return self.bx, self.by

    @property
    def s(self):
        return self.sx, self.sy


def parse_sensor(line: str):
    m = pattern.match(line.strip())
    vals = [int(v) for v in m.groups()]
    sx, sy, bx, by = vals
    d = manhattan_distance((sx, sy), (bx, by))
    return Sensor(*vals, d)


def get_tuning_frequency(x, y):
    return x * 4000000 + y


sensors = [parse_sensor(line) for line in lines if line.strip()]

distress_beacon_bounds = (0, 4000000)

distress_beacon = None
try:
    for query_y in range(distress_beacon_bounds[0], distress_beacon_bounds[1] + 1):
        possible = [distress_beacon_bounds]
        for sensor in sensors:
            # sensor does not concern queried row
            if query_y > sensor.sy + sensor.d or query_y < sensor.sy - sensor.d:
                continue

            dx = sensor.d - abs(query_y - sensor.sy)

            possible = ranges_diff(possible, (sensor.sx - dx, sensor.sx + dx))
            if not possible:
                break

        if len(possible) == 1 and possible[0][0] == possible[0][1]:
            distress_beacon = (possible[0][0], query_y)
            raise StopIteration
except StopIteration:
    pass

print(distress_beacon)
print(get_tuning_frequency(*distress_beacon))
