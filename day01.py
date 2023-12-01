from re import findall

def read_file() -> list[str]:
    with open("input01.txt") as f:
        lines = [x.strip() for x in f.readlines()]
        return lines
    
lines = read_file()


sum = 0
for line in lines:
    digits = [x for x in line if x.isdigit()]
    sum += int(digits[0] + digits[-1])

print(sum)

digit_map = {
    "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
    "six": "6", "seven": "7", "eight": "8", "nine": "9",
}

sum = 0
for line in lines:
    digits = findall("(?=(one|two|three|four|five|six|seven|eight|nine|1|2|3|4|5|6|7|8|9))", line,)    
    sum += int(
        digit_map.get(digits[0], digits[0])
        + digit_map.get(digits[-1], digits[-1]))
    
print(sum)