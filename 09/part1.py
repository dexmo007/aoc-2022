with open('input.txt') as f:
    lines = f.readlines()


def parse_step(line: str):
    direction, n_steps = line.strip().split(' ')
    return direction, int(n_steps)


steps = [parse_step(line) for line in lines]

head_x, head_y = 0, 0
tail_x, tail_y = 0, 0

tail_positions = {(tail_x, tail_y)}


def is_tail_adjacent():
    return abs(head_x - tail_x) <= 1 \
        and abs(head_y - tail_y) <= 1


moves = {
    'R': ((1, 0), (-1, 0)),
    'L': ((-1, 0), (1, 0)),
    'U': ((0, 1), (0, -1)),
    'D': ((0, -1), (0, 1))
}
for (direction, n_steps) in steps:
    (dx, dy), (offset_x, offset_y) = moves[direction]
    for _ in range(n_steps):
        head_x += dx
        head_y += dy
        if not is_tail_adjacent():
            tail_x, tail_y = head_x + offset_x, head_y + offset_y
        tail_positions.add((tail_x, tail_y))

print(len(tail_positions))
