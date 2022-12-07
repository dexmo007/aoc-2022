
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import re

with open('input.txt') as f:
    lines = f.readlines()

commands = []
for line in lines:
    line = line.strip()
    if line.startswith('$'):
        commands.append((line[2:], []))
    else:
        command, results = commands[-1]
        results.append(line)


@dataclass
class Node:
    name: str


@dataclass
class Dir(Node):
    parent: Optional[Dir]
    children: list[Node]


@dataclass
class File(Node):
    size: int


def parse_result(node: Dir, result: str):
    col1, col2 = result.split(' ')
    if col1 == 'dir':
        return Dir(col2, node, [])
    else:
        return File(col2, int(col1))


root = Dir('/', None, [])
node: Dir = None
for command, results in commands:
    if command == 'cd /':
        node = root
    elif command == 'ls':
        for result in results:
            node.children.append(parse_result(node, result))
    elif command == 'cd ..':
        node = node.parent
    else:
        m = re.match(r'cd (.+)', command)
        change_to = m.group(1)
        node = next(c for c in node.children if isinstance(
            c, Dir) and c.name == change_to)


def get_size(dir):
    return sum(child.size if isinstance(child, File)
               else get_size(child) for child in dir.children)


def handle(node: Dir):
    size = get_size(node)
    total = 0
    if size <= 100000:
        total += size
    for c in node.children:
        if isinstance(c, Dir):
            total += handle(c)
    return total


print(handle(root))
