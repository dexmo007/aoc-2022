from __future__ import annotations
from typing import Literal
import os

JetDirection = Literal['<', '>']
Movement = tuple[int, int]
Coords = tuple[int, int]


class Environment:
    def is_blocked(self, coords: Coords) -> bool:
        raise NotImplementedError

    def is_any_blocked(self, coords: list[Coords]) -> bool:
        return any(self.is_blocked(c) for c in coords)


with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as f:
    jet_pattern: list[JetDirection] = f.readlines()[0]

CHAMBER_WIDTH = 7
spawn_offset_x = 2
spawn_offset_y = 3


class Block:
    _coords: Coords
    points: list[Coords]

    def __init__(self, height: int) -> None:
        self._coords = spawn_offset_x, height + spawn_offset_y
        self.points = self.mk_points(*self._coords)

    @property
    def left(self):
        return self._coords[0]

    @left.setter
    def left(self, new_left: int):
        _, b = self._coords
        self._coords = new_left, b
        self.points = self.mk_points(*self._coords)

    @property
    def bottom(self):
        return self._coords[1]

    @bottom.setter
    def bottom(self, new_bottom: int):
        l, _ = self._coords
        self._coords = l, new_bottom
        self.points = self.mk_points(*self._coords)

    def mk_points(self, left: int, bottom: int) -> Coords:
        raise NotImplementedError

    def would_collide(self, movement: Movement, environment: Environment) -> bool:
        dx, dy = movement
        new_points = [(x+dx, y+dy) for x, y in self.points]
        return min(x for x, _ in new_points) < 0 or max(x for x, _ in new_points) >= CHAMBER_WIDTH \
            or min(y for _, y in new_points) < 0 \
            or environment.is_any_blocked(new_points)

    def push_by_jet(self, direction: JetDirection, environment: Environment) -> None:
        if direction == '<':
            if not self.would_collide((-1, 0), environment):
                self.left -= 1
            return
        # direction == '>'
        if not self.would_collide((1, 0), environment):
            self.left += 1

    def fall_down(self, environment: Environment) -> bool:
        if self.would_collide((0, -1), environment):
            return False
        self.bottom -= 1
        return True


class HLine(Block):
    def mk_points(self, left, bottom) -> Coords:
        return [(left + i, bottom) for i in range(4)]


class Cross(Block):
    def mk_points(self, left, bottom) -> Coords:
        return [(left + 1, bottom + 2), (left + 1, bottom)] + [(left + i, bottom + 1) for i in range(3)]


class LShape(Block):
    def mk_points(self, left, bottom) -> Coords:
        return [(left + i, bottom) for i in range(3)] + [(left + 2, bottom + i + 1) for i in range(2)]


class VLine(Block):
    def mk_points(self, left: int, bottom: int) -> Coords:
        return [(left, bottom + i) for i in range(4)]


class Square(Block):
    def mk_points(self, left: int, bottom: int) -> Coords:
        return [(left + i % 2, bottom + i // 2) for i in range(4)]


class BlockEnvironment(Environment):

    blocks: list[Block] = []
    blocked_points: set[Coords] = set()

    def add_block(self, block: Block):
        self.blocks.append(block)
        for p in block.points:
            self.blocked_points.add(p)

    def is_blocked(self, coords: Coords) -> bool:
        return coords in self.blocked_points


block_order = [HLine, Cross, LShape, VLine, Square]

n_blocks = 2022

height = 0

environment = BlockEnvironment()


def print_chamber(block: Block | None = None):
    grid = [['.' for _ in range(CHAMBER_WIDTH)] for _ in range(
        max(height+1, max(y+1 for _, y in block.points)) if block else height+1)]
    for x, y in environment.blocked_points:
        grid[y][x] = '#'
    if block:
        for x, y in block.points:
            grid[y][x] = '@'

    for row in reversed(grid):
        print('|', end='')
        for cell in row:
            print(cell, end='')
        print('|')
    print('+' + ('-' * CHAMBER_WIDTH) + '+')


jet_index = 0
for i in range(n_blocks):
    next_block_cls = block_order[i % len(block_order)]
    new_block: Block = next_block_cls(height)
    # print('new block', new_block, height)
    # print_chamber(new_block)
    while True:
        jet = jet_pattern[jet_index]
        jet_index = (jet_index + 1) % len(jet_pattern)
        new_block.push_by_jet(jet, environment)
        # print('push by jet')
        # print_chamber(new_block)
        fell = new_block.fall_down(environment)
        # print('falls down', 'rest' if not fell else '')
        # print_chamber(new_block)
        if not fell:
            height = max(height, max(y for _, y in new_block.points) + 1)
            environment.add_block(new_block)
            break

    # if i == 9:
    #     break

# print_chamber()
print(height)
