with open('input.txt') as f:
    lines = f.readlines()

grid = []
for line in lines:
    grid.append(list(map(int, line.strip())))


def is_visible(grid, row, col):
    height = grid[row][col]
    left = grid[row][:col]
    right = grid[row][col+1:]
    col_array = [r[col] for r in grid]
    top = col_array[:row]
    bottom = col_array[row+1:]
    return min(max(left), max(right), max(top), max(bottom)) < height


visible = 2 * len(grid) + 2 * (len(grid[0]) - 2)
for row in range(1, len(grid) - 1):
    for col in range(1, len(grid[row]) - 1):
        if is_visible(grid, row, col):
            visible += 1

print(visible)
