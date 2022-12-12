from collections import defaultdict
import math
import time


with open('input.txt') as f:
    lines = f.readlines()


grid = []
target = None

for y, line in enumerate(lines):
    row = []
    for x, cell in enumerate(line.strip()):
        if cell == 'S':
            row.append(0)
            starting_position = x, y
        elif cell == 'E':
            row.append(ord('z') - ord('a'))
            target = x, y
        else:
            row.append(ord(cell) - ord('a'))
    grid.append(row)

Y = len(grid)
X = len(grid[0])


def can_go(from_pos, to_pos):
    x, y = to_pos
    within_bounds = y >= 0 and y < Y and x >= 0 and x < X
    from_x, from_y = from_pos
    return within_bounds and grid[y][x] <= grid[from_y][from_x] + 1


def get_neighbors(pos):
    x, y = pos
    if can_go(pos, (x, y+1)):
        yield (x, y+1)
    if can_go(pos, (x, y-1)):
        yield (x, y-1)
    if can_go(pos, (x+1, y)):
        yield (x+1, y)
    if can_go(pos, (x-1, y)):
        yield (x-1, y)


def heuristic(pos):
    x, y = pos
    target_x, target_y = target
    return abs(target_x - x) - 1 + abs(target_y - y) - 1


def reconstruct_path(came_from: dict[(int, int), (int, int)], current: tuple[int, int]):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return list(reversed(total_path))


def traverse_a_star(starting_position):
    open_set = {starting_position}
    came_from = dict()
    g_score = defaultdict(lambda: math.inf)
    g_score[starting_position] = 0
    f_score = defaultdict(lambda: math.inf)
    f_score[starting_position] = heuristic(starting_position)
    while len(open_set) > 0:
        current = min(open_set, key=lambda n: f_score[n])
        if current == target:
            return reconstruct_path(came_from, current)
        open_set.remove(current)
        for neighbor in get_neighbors(current):
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor)
                open_set.add(neighbor)


start = time.time()

starting_positions = [(x, y) for x in range(X)
                      for y in range(Y) if grid[y][x] == 0]

solutions = [traverse_a_star(starting_position)
             for starting_position in starting_positions]

fewest_steps = min(len(s) - 1 for s in solutions if s is not None)
end = time.time()
print(f"Found the optimal solution after {end - start}")

print(f"Fewest steps: {fewest_steps}")
