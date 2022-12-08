with open('input.txt') as f:
    lines = f.readlines()

grid = []
for line in lines:
    grid.append(list(map(int, line.strip())))


def get_scenic_score(l, r, t, b):
    return l*r*t*b


def get_viewing_distance(height, lane):
    d = 0
    for h in lane:
        d += 1
        if h >= height:
            break
    return d


def get_viewing_distances(grid, row, col):
    height = grid[row][col]
    left = get_viewing_distance(height, reversed(grid[row][:col]))
    right = get_viewing_distance(height, grid[row][col+1:])
    col_array = [r[col] for r in grid]
    top = get_viewing_distance(height, reversed(col_array[:row]))
    bottom = get_viewing_distance(height, col_array[row+1:])
    return left, right, top, bottom


max_scenic_score = -1

for row in range(1, len(grid) - 1):
    for col in range(1, len(grid[row]) - 1):
        viewing_distances = get_viewing_distances(grid, row, col)
        max_scenic_score = max(
            max_scenic_score, get_scenic_score(*viewing_distances))

print(max_scenic_score)
