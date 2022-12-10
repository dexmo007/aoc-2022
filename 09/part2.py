with open('input.txt') as f:
    lines = f.readlines()

PRINT = False


def parse_step(line: str):
    direction, n_steps = line.strip().split(' ')
    return direction, int(n_steps)


steps = [parse_step(line) for line in lines]

N_KNOTS = 10
HEAD = 0
TAIL = N_KNOTS - 1
knots = [(0, 0) for _ in range(N_KNOTS)]

tail_positions = {knots[TAIL]}

moves = {
    'R': (1, 0),
    'L': (-1, 0),
    'U': (0, 1),
    'D': (0, -1)
}

GRID_DIM = ((0, 0), (0, 0))
cursor = 0, 0
for direction, n_steps in steps:
    dx, dy = moves[direction]
    x, y = cursor
    cursor = x + n_steps * dx, y + n_steps * dy
    GRID_DIM = (min(GRID_DIM[0][0], cursor[0]), max(GRID_DIM[0][1], cursor[0])), (min(
        GRID_DIM[1][0], cursor[1]), max(GRID_DIM[1][1], cursor[1]))


def is_knot_adjacent(knot1, knot2):
    x1, y1 = knot1
    x2, y2 = knot2
    return abs(x1 - x2) <= 1 \
        and abs(y1 - y2) <= 1


def print_knots(newline=None):
    if not PRINT:
        return
    cols = GRID_DIM[0][1] - GRID_DIM[0][0] + 1
    rows = GRID_DIM[1][1] - GRID_DIM[1][0] + 1
    offset_x, offset_y = GRID_DIM[0][1] * -1 - 1, GRID_DIM[1][1] * -1 - 1
    grid = [['.' for _ in range(cols)]
            for _ in range(rows)]
    grid[knots[HEAD][1]+offset_y][knots[HEAD][0]+offset_x] = 'H'
    for i, (x, y) in enumerate(knots[1:], 1):
        if grid[y+offset_y][x+offset_x] == '.':
            grid[y+offset_y][x+offset_x] = str(i)
    for x, y in tail_positions:
        if grid[y+offset_y][x+offset_x] == '.':
            grid[y+offset_y][x+offset_x] = '#'
    print('\n'.join(''.join(row) for row in reversed(grid)))
    if newline is not None:
        print(newline)


if PRINT:
    print('== Initial State ==')
    print_knots()

moves = {
    'R': (1, 0),
    'L': (-1, 0),
    'U': (0, 1),
    'D': (0, -1)
}
for (direction, n_steps) in steps:
    if PRINT:
        print(f'== {direction} {n_steps} ==')
    dx, dy = moves[direction]
    for _ in range(n_steps):
        head_x, head_y = knots[HEAD]
        knots[HEAD] = head_x + dx, head_y + dy
        for i in range(1, len(knots)):
            if is_knot_adjacent(knots[i], knots[i-1]):
                break
            x, y = knots[i]
            prev_x, prev_y = knots[i-1]
            adj_x = 1 if prev_x > x else (0 if prev_x == x else -1)
            adj_y = 1 if prev_y > y else (0 if prev_y == y else -1)
            knots[i] = x + adj_x, y + adj_y
        tail_positions.add(knots[TAIL])
        print_knots('\n')
    print_knots()

print(len(tail_positions))
