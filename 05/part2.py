import re

with open('input.txt') as f:
    lines = f.readlines()

stack_config = []
for (i, line) in enumerate(lines):
    if not line.strip():
        separator_line = i
        break
    stack_config.append(line)

n_stacks = int(stack_config[-1].strip().split('   ')[-1])

stacks = [[] for _ in range(n_stacks)]

for line in list(reversed(stack_config))[1:]:
    for i in range(n_stacks):
        item = line[4 * i + 1]
        if item == ' ':
            continue
        stacks[i].append(item)

for line in lines[separator_line+1:]:
    m = re.match(r'move (\d+) from (\d+) to (\d+)', line.strip())
    amount, from_index, to_index = m.groups()
    amount, from_index, to_index = int(amount), int(from_index), int(to_index)
    moved_items = []
    for _ in range(amount):
        moved_items.append(stacks[from_index - 1].pop())
    for item in reversed(moved_items):
        stacks[to_index - 1].append(item)

print(''.join((stack[-1] for stack in stacks)))
