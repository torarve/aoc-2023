from itertools import combinations

def read_file() -> list[str]:
    with open("input11.txt") as f:
        lines = [x.strip() for x in f.readlines()]
        return lines
        
lines = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""".split("\n")

lines = read_file()

data = "".join(lines)
height = len(lines)
width = len(lines[0])

empty_rows = [i for (i,line) in enumerate(lines) if line=="."*width]
empty_cols = [i for i in range(height) if data[i::width]=="."*height]
galaxies = [(x%width, x//width) for (x,c) in enumerate(data) if c=="#"]

def find_total_distance(factor=2):
    sum_distance = 0
    for a, b in combinations(galaxies, 2):
        tmp = abs(a[0]-b[0]) + abs(a[1]-b[1])
        max_x = max(a[0], b[0])
        min_x = min(a[0], b[0])
        max_y = max(a[1], b[1])
        min_y = min(a[1], b[1])
        num_extra_cols = len([x for x in empty_cols if min_x<x and x<max_x])
        num_extra_rows = len([y for y in empty_rows if min_y<y and y<max_y])
        sum_distance += tmp + num_extra_cols*(factor-1) + num_extra_rows*(factor-1)
    return sum_distance    

print(find_total_distance())
print(find_total_distance(1000000))
