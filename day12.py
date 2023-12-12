def read_file() -> list[str]:
    with open("input12.txt") as f:
        lines = [x.strip() for x in f.readlines()]
        return lines
    
def parse_line(line: str) -> tuple[str, tuple[int]]:
    left, right = line.split(" ")
    nums = [int(x) for x in right.split(",")]
    return left, tuple(nums)


def find_valid_prefixes(line: str, groups: tuple[int], cache = {}, prev=""):
    state = f"{line}:{':'.join([str(x) for x in groups])}"
    if state in cache:
        return cache[state]

    if len(groups) == 0:
        return 1 if line.find("#")<0 else 0

    g = groups[0]
    start = 0
    remaining = 0 if len(groups)==1 else sum(groups[1:]) + len(groups[1:]) - 1
    if remaining<0:
        pass
    remaining = sum(groups[1:]) + len(groups[1:]) -1
    end = len(line) - (remaining + g)
    tmp = ["."*(j-start) + "#"*g for j in range(start, end)]
    count = 0
    for prefix in tmp:
        if len(prefix)<len(line):
            prefix += "." # Must be seperated
        valid = True
        for i, c in enumerate(prefix):
            if line[i]!="?" and line[i] != prefix[i]:
                valid = False
        if valid:
            count += find_valid_prefixes(line[len(prefix):], groups[1:], cache, prev+prefix)

    cache[state] = count
    return count

def find_solution(lines):
    total_count = 0
    for i, (line, groups) in enumerate(lines):
        total_count += find_valid_prefixes(line, groups)
    return total_count

lines = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""".split("\n")

lines = read_file()
lines = [parse_line(x) for x in lines]

print(find_solution(lines))

lines = [("?".join([line]*5), group*5) for line, group in lines]

print(find_solution(lines))

