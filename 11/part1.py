import math
from dataclasses import dataclass
import re
from typing import Callable


@dataclass
class Monkey:
    items: list[int]
    operation: Callable[[int], int]
    test_divisor: int
    true_target: int
    false_target: int


pattern = re.compile(r"""Monkey \d+:
  Starting items: (?P<items>.+)
  Operation: new = old (?P<op>\*|\+) (?P<operand>old|\d+)
  Test: divisible by (?P<test_divisor>\d+)
    If true: throw to monkey (?P<true_target>\d+)
    If false: throw to monkey (?P<false_target>\d+)""", re.MULTILINE)

monkeys: list[Monkey] = []


def parse_operation(op, operand):
    if op == '*':
        if operand == 'old':
            return lambda old: old * old
        factor = int(operand)
        return lambda old, factor=factor: old * factor
    if operand == 'old':
        return lambda old: old + old
    summand = int(operand)
    return lambda old, summand=summand: old + summand


def parse_monkey(definition: str) -> Monkey:
    m = re.match(pattern, definition)
    items = [int(item.strip()) for item in m.group('items').split(',')]
    operation = parse_operation(m.group('op'), m.group('operand'))
    return Monkey(items, operation,
                  test_divisor=int(m.group('test_divisor')),
                  true_target=int(m.group('true_target')),
                  false_target=int(m.group('false_target'))
                  )


current_monkey_def = ""
with open('input.txt') as f:
    for line in f:
        if not line.strip():
            monkeys.append(parse_monkey(current_monkey_def))
            current_monkey_def = ""
        else:
            current_monkey_def += line
monkeys.append(parse_monkey(current_monkey_def))

N_ROUNDS = 20

total_inspections = [0 for _ in range(len(monkeys))]

for round in range(N_ROUNDS):
    for i, monkey in enumerate(monkeys):
        for worry_level in monkey.items:
            worry_level = monkey.operation(worry_level)
            total_inspections[i] += 1
            worry_level = worry_level // 3
            if worry_level % monkey.test_divisor == 0:
                target = monkey.true_target
            else:
                target = monkey.false_target
            monkeys[target].items.append(worry_level)
        monkey.items = []

print(math.prod(sorted(total_inspections, reverse=True)[:2]))
