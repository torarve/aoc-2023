from itertools import permutations
from re import match
import re


def read_file() -> list[str]:
    with open("input12.txt") as f:
        lines = [x.strip() for x in f.readlines()]
        return lines
    
lines = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""".split("\n")

print(lines)

lines = read_file()

def check(c: str) -> bool | None:
    match c:
        case ".": return False
        case "#": return True
        case "?": return None
        
    raise "Not possible"

def parse_line(line: str) -> tuple[str, tuple[int]]:
    left, right = line.split(" ")
    nums = [int(x) for x in right.split(",")]
    return left, tuple(nums)

def check_arrangements(line: str) -> tuple[int]:
    m = re.findall("#+", line)
    return tuple([len(x) for x in m])

def replace(line: str, pos: list[int]) -> str:
    if len(pos)==0: 
        yield line
    else:
        for i in replace(line, pos[1:]):
            yield i[:pos[0]] + "." + i[pos[0]+1:]
            yield i[:pos[0]] + "#" + i[pos[0]+1:]


def find_all_possible_arrangements(lines) -> int:
    total_count = 0
    for i, (line, groups) in enumerate(lines):
        print(f"{i+1} of {len(lines)}")
        count = 0
        # line, groups = parse_line(line)
        tmp = [i for (i, x) in enumerate(line) if x == "?"]
        for l in replace(line, tmp):
            a = check_arrangements(l)
            if a == groups:
                count += 1
        total_count += count
    return total_count




def is_possible_match(line: str, groups: tuple[int]) -> bool:
    a = check_arrangements(line)
    if len(a)>len(groups):
        return False
    if len(a) == 0:
        return True
    l = len(a)-1
    if l == 0:
        pass
    
    return a[:l] == groups[:l] and a[l]<=groups[l] 

def replace2(line: str, pos: list[int], groups: tuple[int]) -> str:
    if len(pos)==0:
        a = check_arrangements(line)
        if a == groups:
            return 1
        else:
            return 0
    
    p = pos[0]
    count = 0
    for c in [".", "#"]:
        tmp =  line[:p] + c + line[p+1:]
        if is_possible_match(tmp[:p+1], groups):
            count += replace2(tmp, pos[1:], groups)
        else:
            pass
            
    return count

def find_all_possible_arrangements_fast(lines: list[tuple[str, tuple[int]]]) -> int:
    total_count = 0
    for i, (line, groups) in enumerate(lines):
        print(f"{i+1} of {len(lines)}")
        tmp = [i for (i, x) in enumerate(line) if x == "?"]
        count = replace2(line, tmp, groups)
        # print(count)
        total_count += count
        
    # print(total_count)
    return total_count
    
lines = [parse_line(x) for x in lines]
print(find_all_possible_arrangements_fast(lines))

lines = [("?".join([line]*5), group*5) for line, group in lines]
print(find_all_possible_arrangements_fast(lines))
