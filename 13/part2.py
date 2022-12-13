import functools

with open('input.txt') as f:
    lines = f.readlines()


def parse_packet(s: str):
    s = s.strip()
    stack = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == '[':
            stack.append([])
            i += 1
            continue
        if c.isdigit():
            digits = c
            i += 1
            while s[i].isdigit():
                digits += s[i]
                i += 1
            stack[-1].append(int(digits))
            continue
        if c == ',':
            i += 1
            continue
        if c == ']':
            top = stack.pop()
            if len(stack) == 0:
                return top
            stack[-1].append(top)
            i += 1
            continue


packets = []
for line in lines:
    if not line.strip():
        continue
    packets.append(parse_packet(line))

dividers = [[[2]], [[6]]]
packets.extend(dividers)


def compare(left, right):
    for i in range(min(len(left), len(right))):
        l = left[i]
        r = right[i]
        if isinstance(l, int) and isinstance(r, int):
            if l < r:
                return -1
            if l > r:
                return 1
        elif isinstance(l, list) and isinstance(r, list):
            res = compare(l, r)
            if res == -1 or res == 1:
                return res
        else:
            l = l if isinstance(l, list) else [l]
            r = r if isinstance(r, list) else [r]

            res = compare(l, r)
            if res == -1 or res == 1:
                return res
    if len(left) < len(right):
        return -1
    if len(left) > len(right):
        return 1
    return 0


decoder_key = 1
for i, packet in enumerate(sorted(packets, key=functools.cmp_to_key(compare)), 1):
    if packet in dividers:
        decoder_key *= i

print(decoder_key)
