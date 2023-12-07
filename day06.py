

from functools import reduce
from operator import mul
import re

def read_file() -> list[str]:
    with open("input06.txt") as f:
        lines = [x.strip() for x in f.readlines()]
        return lines

lines = """Time:      7  15   30
Distance:  9  40  200""".split("\n")


lines = read_file()

times = [int(x) for x in re.findall(r"\d+", lines[0][len("Time:"):])]
records = [int(x) for x in re.findall(r"\d+", lines[1][len("Distance:"):])]


def calc_distance(speed: int, time: int) -> int:
    return speed*time
    
all_wins = []
for i in range(len(times)):
    wins = 0
    for j in range(times[i]):
        if calc_distance(j, times[i]-j) > records[i]:
            wins += 1
    all_wins.append(wins)
    
print(reduce(mul,all_wins))

time = int(lines[0][len("Time:"):].replace(" ", ""))
record = int(lines[1][len("Distance:"):].replace(" ", ""))

result = 0
for i in range(time):
    if calc_distance(i, time-i)>record:
        result += 1
print(result)
