with open('input.txt') as f:
    lines = f.readlines()

elves = []
current = []
for line in lines:
    if line.strip():
        current.append(int(line.strip()))
    else:
        elves.append(current)
        current = []
elves.append(current)

print(sum(sorted(map(lambda elf: sum(elf), elves), reverse=True)[:3]))
