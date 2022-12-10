with open('input.txt') as f:
    lines = f.readlines()


def parse_instruction(line: str):
    line = line.strip()
    if line == 'noop':
        return ('noop', 1)
    op, V = line.split(' ')
    return op, 2, int(V)


instructions = [parse_instruction(line) for line in lines]

X = 1
cycle = 1
pixel = 0


def draw():
    global pixel
    pixel_value = '#' if pixel >= X - 1 and pixel <= X + 1 else '.'
    print(pixel_value, end='')
    pixel = (pixel + 1) % 40
    if pixel == 0:
        print()


for op, cycles, *args in instructions:
    for i in range(cycles - 1):
        draw()
        cycle += 1
    draw()
    if op == 'noop':
        pass
    elif op == 'addx':
        V, = args
        X += V
    cycle += 1
