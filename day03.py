import re


def read_file() -> list[str]:
    with open("input03.txt") as f:
        lines = [x.strip() for x in f.readlines()]
        return lines

lines = ["467..114..",
"...*......",
"..35..633.",
"......#...",
"617*......",
".....+.58.",
"..592.....",
"......755.",
"...$.*....",
".664.598.."
]
lines = read_file()

result = []
for i, line in enumerate(lines):
    for m in re.finditer("\d+", line):
        start = m.start(0)
        end = m.end(0)
        number = line[start:end]
        adjacent = ""
        if start > 0:
            adjacent += line[start-1]
        if i > 0: # Check above
            above = lines[i-1][max(start-1, 0):min(end+1, len(line))]
            adjacent += above
        if end < len(lines):
            adjacent += line[end]
        if i < len(lines)-1: # Check below
            below = lines[i+1][max(start-1, 0):min(end+1, len(line))]
            adjacent += below
        if len([x for x in adjacent if x != "." and not x.isdigit()]):
            result.append(int(number))
            
print(sum(result))

def extract_number_at(pos: int, line: str):
    start, end = pos, pos
    while start>0 and line[start-1].isdigit():
        start -= 1
    while end<len(line) and line[end].isdigit():
        end += 1
        
    return int(line[start:end])

def find_digits_on_line(line, start, end):
    result = []
    for m in re.finditer(r"\d+", line):
        if not (m.start(0)>end or m.end(0)-1<start):
            tmp = line[m.start(0):m.end(0)]
            result.append(int(tmp))
    return result
            

result = []
for i, line in enumerate(lines):
    for m in re.finditer("\\*", line):
        digits = []
        start = m.start(0)
        end = m.end(0)
        if start>0 and line[start-1].isdigit():
            digits.append(extract_number_at(start-1, line))
        if i>0:
            digits.extend(find_digits_on_line(lines[i-1], max(0, start-1), min(end, len(line)-1)))
        if end<len(line) and line[end].isdigit():
            digits.append(extract_number_at(end, line))
        if i<len(lines)-1:
            digits.extend(find_digits_on_line(lines[i+1], max(0, start-1), min(end, len(line)-1)))
        
        if len(digits)==2:
            result.append(digits[0] * digits[1])

print(sum(result))
