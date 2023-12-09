from itertools import accumulate
from operator import sub


def read_file() -> list[str]:
    with open("input09.txt") as f:
        lines = [x.strip() for x in f.readlines()]
        return lines


lines = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45""".split("\n")

lines = read_file()

report = [[int(x) for x in line.split(" ")]
          for line in lines]

sum = 0
sum2 = 0
for history in report:
    diffs = [history]
    current = history
    while any([x!=0 for x in current]):
        current = [current[i+1]-current[i] 
                for i in range(len(current)-1)]
        diffs.append(current)
        
    result = 0
    result2 = 0
    for i in range(len(diffs)):
        # Part 1
        result = diffs[-i][-1] + result
        # Part 2
        result2 = diffs[-(i+1)][0] - result2
        
    sum += result
    sum2 += result2
    
print(sum)
print(sum2)