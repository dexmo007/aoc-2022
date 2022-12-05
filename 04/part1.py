with open('input.txt') as f:
    lines = f.readlines()


def parse_range(s: str):
    start, end = s.split('-')
    return int(start), int(end)


def range_contains(r1, r2):
    start1, end1 = r1
    start2, end2 = r2
    return start2 >= start1 and end2 <= end1


fully_contained_ranges = 0
for line in lines:
    first, second = line.strip().split(',')
    first = parse_range(first)
    second = parse_range(second)
    if range_contains(first, second) or range_contains(second, first):
        fully_contained_ranges += 1


print(fully_contained_ranges)
