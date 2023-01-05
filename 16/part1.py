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
class Valve:
    idx: int
    id: str
    flow_rate: int
    connections: list[tuple[str, int]]

    def __hash__(self) -> int:
        return hash(self.id)


def parse_valve(idx: int, s: str):
    m = pattern.match(s.strip())
    id, flow_rate, connections = m.groups()
    return Valve(idx, id, int(flow_rate), [(c.strip(), 1) for c in connections.split(',')])


start_position = 'AA'
valves = [parse_valve(idx, line) for idx, line in enumerate(lines)]
valves = {v.id: v for v in valves}

# optimize graph: removes valves of zero flow_rate (other than the starting position)
while sum(1 for v in valves.values() if v.flow_rate == 0 and v.id != start_position) > 0:
    valve = next(v for v in valves.values() if v.flow_rate ==
                 0 and v.id != start_position)
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

# update index because we deleted valves
for new_idx, valve in enumerate(valves.values()):
    valve.idx = new_idx

max_valves_to_open_mask = reduce(lambda acc, cur: acc if cur.flow_rate == 0 else (
    acc | (2**cur.idx)), valves.values(), 0)
max_valves_to_open = max_valves_to_open_mask.bit_count()

max_possible_pressure = sum(v.flow_rate for v in valves.values())

max_time = 30
max_pressure = None
n_solutions_proposed = 0
partial_solutions = [
    (max_time, (None, valves[start_position]), (0, list(sorted((v.flow_rate for v in valves.values()), reverse=True))), False, 0, 0)]


def propose_solution(pressure):
    global n_solutions_proposed, max_pressure
    n_solutions_proposed += 1
    if max_pressure is None or pressure > max_pressure:
        max_pressure = pressure
        return


def get_optimistic_future_pressure_if_open(valves_to_open: list[int], time_left: int):
    # if current valve open, assume we can walk, open, repeat in the best possible order
    # we reach this pressure
    pressure = 0
    for i, flow_rate in enumerate(itertools.islice(valves_to_open, time_left // 2), 1):
        pressure += (time_left - 2*i) * flow_rate
    return pressure


def get_optimistic_future_pressure_if_closed(current_position: Valve, valves_to_open: list[int], new_valves_to_open: list[int], time_left: int):
    # we can either open this then walk open repeat in best order
    open_first_pressure = (time_left - 1) * current_position.flow_rate
    for i, flow_rate in enumerate(itertools.islice(new_valves_to_open, (time_left-1) // 2), 1):
        open_first_pressure += (time_left - 2*i - 1) * flow_rate
    # or walk open repeat in best order
    walk_first_pressure = 0
    for i, flow_rate in enumerate(itertools.islice(valves_to_open, time_left // 2), 1):
        walk_first_pressure += (time_left - 2*i) * flow_rate
    return max(open_first_pressure, walk_first_pressure)


start = time.time()

while len(partial_solutions) > 0:
    new_partial_solutions = []
    for time_left, positions, valve_state, allow_going_back, current_pressure, pressure in partial_solutions:
        if time_left == 0:
            propose_solution(pressure)
            continue
        open_valves, valves_to_open = valve_state
        last_connection, current_position = positions
        current_mask = 2 ** current_position.idx
        current_open = bool(open_valves & current_mask)
        pressure_prognosis = pressure + time_left * current_pressure
        if not current_open and current_position.flow_rate > 0:
            new_valves_to_open = valves_to_open[:]
            new_valves_to_open.remove(current_position.flow_rate)
            # if max_pressure cannot possible be reached be can discard this solution proposal
            if max_pressure is not None and pressure_prognosis + get_optimistic_future_pressure_if_closed(current_position, valves_to_open, new_valves_to_open, time_left) <= max_pressure:
                continue
            new_open_valves = open_valves | current_mask
            propose_solution(pressure + current_pressure + (time_left-1) *
                             (current_pressure + current_position.flow_rate))
            # if last non-zero valve was opened we do not need to progress further
            if new_open_valves == max_valves_to_open_mask:
                continue
            new_partial_solutions.append(
                (time_left - 1, positions, (new_open_valves, new_valves_to_open), True, current_pressure + current_position.flow_rate, pressure + current_pressure))
        elif max_pressure is not None and pressure_prognosis + get_optimistic_future_pressure_if_open(valves_to_open, time_left) <= max_pressure:
            continue
        connections = current_position.connections[:]
        if last_connection is not None and not allow_going_back:
            # don't move back without doing anything
            connections.remove(last_connection)
        for target, weight in connections:
            # skip connection if no more time left (at least 1 more minute is needed to do something after movement)
            if time_left <= weight:
                continue
            target_valve = valves[target]
            target_open = (open_valves & (2**target_valve.idx))
            # if we have time to open 1 more valve, we don't need to move to valve that are already open
            if time_left == weight + 1 and target_open:
                continue
            # if target is open and dead end, there is no point in moving there
            if target_open and len(target_valve.connections) == 1:
                continue
            new_partial_solutions.append((time_left - weight, ((current_position.id, weight), target_valve),
                                         valve_state, False, current_pressure, pressure + weight * current_pressure))
    partial_solutions = new_partial_solutions

took = time.time() - start
print(f'Analyzed {n_solutions_proposed} solutions in {took} seconds')

print('=============')

print(max_pressure)

# Sample input
# ============
# base                         8.2M in 32s
# open_valves as set           8.2M in 30s
# open_vales ref               unchanged
# break on all open            7.9M in 29s
# reduced graph + refactor     500k in 7.5s
# current_pressure             500k in 5.5s
# bitmask                      500k in 4.6s
# abort if max cant be reached 1612 in 0.01s
# optimistic future pressure   1372 in 0.014s
# memorize valves to open      1372 in 0.011s
# correct opt fut pressure      884 in 0.00853s
# even better opt fut pres      776 in 0.00548s


# Actual input
# ============
# base                        4.5M in 65s
# optimistic future pressure  280k in 10s
# memorize valves to open     280k in 7.2s
# correct opt fut pressure    20k in 0.3s
# even better opt fut pres    14k in 0.3s
