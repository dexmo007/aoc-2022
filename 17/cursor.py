

blocks = set()
raw = """
   #
  ###
   #
  ### ###
 ######
#    ##
"""
chamber_width = 9


def print_blocks(blocks, mark=None):
    max_y = max(y for _, y in blocks)
    for y in range(max_y, 0, -1):
        print('|', end='')
        for x in range(chamber_width):
            print('@' if mark and (x, y) == mark else '#' if (x, y) in blocks else '.', end='')
        print('|')
    print('+' + (''.join('@' if mark and (x, 0) == mark else '-' for x in range(chamber_width))) + '+')


y = 1
for line in reversed(raw.splitlines()):
    if not line.strip():
        continue

    for x, c in enumerate(line):
        if c == '#':
            blocks.add((x, y))
    y += 1

print_blocks(blocks)

new_blocks = set()
start_y = min((y for x, y in blocks if x == 0), default=0)
x, y = 0, start_y
if y != 0:
    new_blocks.add((x, y))

rotation = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
n_rotations = len(rotation)
direction = 1
while x < chamber_width - 1:
    for _ in range(n_rotations):
        dx, dy = rotation[direction]
        nx, ny = x+dx, y+dy
        if ny == 0 or (nx, ny) in blocks:
            x, y = nx, ny
            # if not straight, turn back 2
            if (dx+dy) % 2 == 0:
                direction = (direction - 2) % n_rotations
            else:
                # if straight, turn back 1
                direction = (direction - 1) % n_rotations
            break
        direction = (direction + 1) % n_rotations
    if y != 0:
        new_blocks.add((x, y))

print(new_blocks)

print_blocks(new_blocks)

max_y = max(y for _, y in blocks)
for y in range(max_y, 0, -1):
    print('|', end='')
    for x in range(chamber_width):
        print('@' if (x, y) in new_blocks else '#' if (x, y) in blocks else '.', end='')
    print('|')
print('+' + ('-'*chamber_width) + '+')
