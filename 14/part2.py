
def tadd(t1, t2):
    x1, y1 = t1
    x2, y2 = t2
    return x1+x2, y1+y2


def sign(x):
    return 0 if x == 0 else 1 if x > 0 else -1


def get_direction(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    dx = x2-x1
    dy = y2-y1
    return sign(dx), sign(dy)


with open('input.txt') as f:
    lines = f.readlines()


def parse_point(s: str):
    x, y = s.split(',')
    return int(x), int(y)


ROCK = '#'
SAND = 'o'
AIR = '.'

stones = []
for line in lines:
    if not line.strip():
        continue
    paths = line.strip().split(' -> ')
    stones.append([parse_point(path) for path in paths])

sand_spawn_x = 500
max_y = max(y for path in stones for x, y in path)
floor_y = max_y + 2
max_floor_length = 2 * floor_y + 1
min_x = min(sand_spawn_x - floor_y, min(x for path in stones for x, y in path))
max_x = max(sand_spawn_x + floor_y, max(x for path in stones for x, y in path))
grid = [[AIR for _ in range(max_x - min_x + 1)] for _ in range(floor_y + 1)]


def update(coords, value):
    global grid
    x, y = coords
    grid[y][x] = value


# add floor
for x in range(max_floor_length):
    update((x, floor_y), ROCK)

# re-adjust x coord
stones = [[tadd(p, (-min_x, 0)) for p in stone] for stone in stones]


def print_grid():
    for row in grid:
        for cell in row:
            print(cell, end='')
        print()


for stone in stones:
    previous = None
    for x, y in stone:
        if previous is None:
            grid[y][x] = ROCK
        else:
            dir = get_direction(previous, (x, y))
            current = tadd(previous, dir)
            while current != (x, y):
                update(current, ROCK)
                current = tadd(current, dir)
            update(current, ROCK)
        previous = (x, y)


def out_of_bounds(x, y):
    return y < 0 or y >= len(grid) or x < 0 or x >= len(grid[y])


def is_blocked(x, y):
    return (not out_of_bounds(x, y)) and grid[y][x] in [ROCK, SAND]


def fall_sand(x, y):
    global grid
    if not is_blocked(x, y+1):
        grid[y][x] = AIR
        if out_of_bounds(x, y+1):
            return True
        grid[y+1][x] = SAND
        return (x, y+1)
    if not is_blocked(x-1, y+1):
        grid[y][x] = AIR
        if out_of_bounds(x-1, y+1):
            return True
        grid[y+1][x-1] = SAND
        return (x-1, y+1)
    if not is_blocked(x+1, y+1):
        grid[y][x] = AIR
        if out_of_bounds(x+1, y+1):
            return True
        grid[y+1][x+1] = SAND
        return (x+1, y+1)
    return None


sand_spawn = sand_spawn_x - min_x, 0

try:
    while not is_blocked(*sand_spawn):
        new_sand = sand_spawn
        update(new_sand, SAND)
        while True:
            new_sand = fall_sand(*new_sand)
            if new_sand is True:
                raise StopIteration
            if new_sand is None:
                break
except StopIteration:
    pass

n_sand = sum(1 if c == SAND else 0 for row in grid for c in row)

print_grid()

print(n_sand)
