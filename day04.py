def read_file() -> list[str]:
    with open("input04.txt") as f:
        lines = [x.strip() for x in f.readlines()]
        return lines

import re

lines = [
    "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
    "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
    "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
    "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
    "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
    "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"
]

lines = read_file()

def parse_line(line: str) -> int:
    idx = line.index(":")
    a, b = tuple(line[idx+1:].split(" | "))
    winning_numbers = [int(x) for x in re.split(r"\W+", a.strip(" "))]
    numbers = [int(x) for x in re.split(r"\W+", b.strip(" "))]
    return winning_numbers, numbers

part1 = 0
for line in lines:
    winning_numbers, numbers = parse_line(line)
    matches = [x for x in numbers if x in winning_numbers]
    if len(matches)>0:
        part1 += (1<<(len(matches)-1))

print(part1)

cards = [parse_line(line) for line in lines]
copies = [1]*len(lines)

for i in range(len(cards)):
    if copies[i]>0:
        winning_numbers, numbers = cards[i]
        matches = [x for x in numbers if x in winning_numbers]
        for j in range(len(matches)):
            copies[i+j+1] += copies[i]
        
print(sum(copies))