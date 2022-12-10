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

cycles_to_sample = {20, 60, 100, 140, 180, 220}
signal_strength = 0


def sample():
    global signal_strength
    if cycle not in cycles_to_sample:
        return
    signal_strength += cycle * X
    #print(f"during {cycle}: X={X}")


for op, cycles, *args in instructions:
    for i in range(cycles - 1):
        sample()
        cycle += 1
    sample()
    if op == 'noop':
        pass
    elif op == 'addx':
        V, = args
        X += V
    cycle += 1

print(signal_strength)
