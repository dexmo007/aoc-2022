with open('input.txt') as f:
    lines = f.readlines()

buffer = lines[0].strip()

N_DISTINCT_CHARS = 14

for i in range(len(buffer) - N_DISTINCT_CHARS):
    maybe_marker = buffer[i:i+N_DISTINCT_CHARS]
    if len({c for c in maybe_marker}) == N_DISTINCT_CHARS:
        print(i+N_DISTINCT_CHARS)
        break
