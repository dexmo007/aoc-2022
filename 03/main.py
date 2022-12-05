with open('input.txt') as f:
    lines = f.readlines()


def priority(c: str):
    if c == c.lower():
        return ord(c) - ord('a') + 1
    return ord(c) - ord('A') + 27


groups = []
current = []
for line in lines:
    current.append(line.strip())
    if len(current) == 3:
        groups.append(current)
        current = []


result = 0
for [first, second, third] in groups:
    for c in first:
        if c in second and c in third:
            result += priority(c)
            break

print(result)
