with open('input.txt') as f:
    lines = f.readlines()

buffer = lines[0].strip()

for i in range(len(buffer) - 4):
    maybe_marker = buffer[i:i+4]
    if len({c for c in maybe_marker}) == 4:
        print(i+4)
        break
