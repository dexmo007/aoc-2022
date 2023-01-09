from __future__ import annotations
from queue import PriorityQueue
from typing import Union
import math
from functools import reduce
import time
import re
import os
from dataclasses import dataclass
import itertools

with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as f:
    lines = f.readlines()


pattern = re.compile(
    r'^Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (.*)$')


@dataclass
class ValveInfo:
    id: str
    flow_rate: int
    connections: list[tuple[str, int]]

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass
class Valve:
    idx: int
    id: str
    flow_rate: int
    connections: list[tuple[Valve, int]]
    is_dead_end: bool
    is_one_way: bool
    min_weight: int

    def __hash__(self) -> int:
        return self.idx

    def __str__(self) -> str:
        connections = ','.join(f"({c.id},{w})" for c, w in self.connections)
        return f"Valve({self.idx},{self.id},flow_rate={self.flow_rate},connections=[{connections}],is_dead_end={self.is_dead_end},is_one_way={self.is_one_way})"

    def __repr__(self) -> str:
        return self.__str__()

    def __lt__(self, other):
        return self.id < other.id


def valve_sort_key(v: Union[ValveInfo, Valve]):
    return v.flow_rate


def parse_valve(s: str):
    m = pattern.match(s.strip())
    id, flow_rate, connections = m.groups()
    return ValveInfo(id, int(flow_rate), [(c.strip(), 1) for c in connections.split(',')])


start_valve_id = 'AA'
valves = [parse_valve(line) for line in lines]
valves = {v.id: v for v in valves}

# optimize graph: removes valves of zero flow_rate (other than the starting position)
while any(v.flow_rate == 0 and v.id != start_valve_id for v in valves.values()):
    valve = next(v for v in valves.values() if v.flow_rate ==
                 0 and v.id != start_valve_id)
    for left, right in itertools.combinations(valve.connections, 2):
        left_id, left_weight = left
        left_valve = valves[left_id]
        right_id, right_weight = right
        right_valve = valves[right_id]
        left_valve.connections.remove((valve.id, left_weight))
        right_valve.connections.remove((valve.id, right_weight))
        left_right_connection = sum(
            weight for id, weight in left_valve.connections if id == right_id)
        # connection left to right not in left.connections or this is cheaper
        if left_right_connection == 0 or left_right_connection > left_weight + right_weight:
            left_valve.connections.append(
                (right_id, left_weight + right_weight))
            right_valve.connections.append(
                (left_id, left_weight + right_weight))
        del valves[valve.id]

# create real Valves, indexed in ascending order of flow_rate
valves = [Valve(idx, valve.id, valve.flow_rate, valve.connections, is_dead_end=len(
    valve.connections) == 1, is_one_way=False, min_weight=min(w for _, w in valve.connections)) for idx, valve in enumerate(sorted(valves.values(), key=valve_sort_key, reverse=True))]

valves_dict = {v.id: v for v in valves}

# set valve refs
for v in valves:
    v.connections = [(valves_dict[c], w) for c, w in v.connections]

# calculate one-way flag
for valve in valves:
    if not valve.is_dead_end:
        continue
    valve.is_one_way = True
    last_valve = valve
    current_valve = valve.connections[0][0]
    while len(current_valve.connections) == 2:
        current_valve.is_one_way = True
        last_valve, current_valve = current_valve, next(
            v for v, _ in current_valve.connections if v != last_valve)


def dijkstra(source: Valve):
    distances = [math.inf] * len(valves)
    distances[source.idx] = 0
    q = set(valves)
    while len(q) > 0:
        u = min(q, key=lambda v: distances[v.idx])
        q.remove(u)
        for v, weight in u.connections:
            if v not in q:
                continue
            alt = distances[u.idx] + weight
            if alt < distances[v.idx]:
                distances[v.idx] = alt
    return distances


# calculate minimum cost paths for each valve to each other valve
distances = []
for v in valves:
    d = dijkstra(v)
    distances.append(d)


def get_next_targets(traversers: list[tuple[int, Valve]], current_mask: int) -> list[list[tuple[int, Valve, int]]]:
    if not current_mask:
        return []
    targets = []
    any_possible = False
    for time_left, current in traversers:
        if time_left <= 2:
            targets.append([(time_left, None, 0)])
            continue
        any_possible = True
        traverser_targets = []
        mask = current_mask
        i = 0
        while mask:
            if mask & 1:
                d = distances[current.idx][i]
                if d + 1 < time_left:  # walk there, open and use pressure at least once
                    target = valves[i]
                    new_time_left = time_left - d - 1
                    traverser_targets.append((new_time_left, target, new_time_left * target.flow_rate))
            i += 1
            mask >>= 1
        targets.append(traverser_targets)
    if not any_possible:
        return []
    return targets


def get_optimistic_pressure_prognosis(traversers, mask):
    i = 0
    pressure = 0
    q = PriorityQueue()
    for t, _ in traversers:
        q.put((-t, t))
    while mask and not q.empty():
        if mask & 1:
            valve = valves[i]
            _, time_left = q.get()
            time_left -= 2
            pressure += valve.flow_rate * time_left
            if time_left > 2:
                q.put((-time_left, time_left))
        i += 1
        mask >>= 1
    return pressure


def unique_product(left, right, respect_order=True, key=lambda x: x):
    if respect_order:
        for l in left:
            for r in right:
                lkey = key(l)
                rkey = key(r)
                if lkey == rkey:
                    continue
                yield (l, r)
    else:
        seen = set()
        for l in left:
            for r in right:
                lkey = key(l)
                rkey = key(r)
                if lkey == rkey:
                    continue
                if (rkey, lkey) in seen:
                    continue
                seen.add((lkey, rkey))
                yield (l, r)


max_time = 26
start_valve = next(v for v in valves if v.id == start_valve_id)
initial_mask = (2**len(valves)-1) ^ (1 << start_valve.idx)


def solve(n_traversers=2):
    max_pressure = 0
    traversers = [(max_time, start_valve) for _ in range(n_traversers)]
    paths = [(traversers, initial_mask, 0)]
    start = time.time()
    first_run = True
    n_iterations = 0
    while len(paths) > 0:
        n_iterations += 1
        traversers, mask, pressure = paths.pop()
        if pressure + get_optimistic_pressure_prognosis(traversers, mask) <= max_pressure:
            continue
        next_targets_per_traverser = get_next_targets(traversers, mask)
        if not next_targets_per_traverser:
            max_pressure = max(max_pressure, pressure)
            continue
        for new_traversers in unique_product(*next_targets_per_traverser, respect_order=not first_run, key=lambda t: t[1]):
            new_mask = mask
            new_pressure = pressure
            new_traverser_states = []
            for time_left, target, added_pressure in new_traversers:
                if target is not None:
                    new_mask ^= 1 << target.idx
                    new_pressure += added_pressure
                new_traverser_states.append((time_left, target))
            paths.append((new_traverser_states, new_mask, new_pressure))
        first_run = False

    print(f"{n_iterations} iterations in {time.time() - start}")
    print('max_pressure=', max_pressure)


solve()
