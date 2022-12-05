with open('input.txt') as f:
    lines = f.readlines()


def parse_range(s: str):
    start, end = s.split('-')
    return int(start), int(end)


def range_overlaps(r1, r2):
    start1, end1 = r1
    start2, end2 = r2
    return start1 >= start2 and start1 <= end2 \
        or end1 >= start2 and end1 <= end2 \
        or start1 <= start2 and end1 >= end2


overlapping_ranges = 0
for line in lines:
    first, second = line.strip().split(',')
    first = parse_range(first)
    second = parse_range(second)
    if range_overlaps(first, second):
        overlapping_ranges += 1


print(overlapping_ranges)
