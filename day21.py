from functools import cache


def read_file() -> list[str]:
    with open("input21.txt") as f:
        lines = [x.strip() for x in f.readlines()]
        return lines


lines = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........""".split("\n")

lines = read_file()

map = "".join(lines)

width = len(lines[0])
height = len(lines)

def solve(steps: int, start:tuple[int,int]) -> int:
    current = set([start])
    for i in range(steps):
        next = []
        for p in current:
            xx, yy = p
            l = (xx-1, yy)
            u = (xx, yy-1)
            r = (xx+1, yy)
            d = (xx, yy+1)
            next.extend([p for p in [l, u, r, d] 
                    if 0<=p[0] and p[0]<width 
                    and 0<=p[1] and p[1]<height
                    and lines[p[1]][p[0]]!="#"])
        current = set(next)
    return len(current)

p = map.find("S")
x, y = (p%width, p//width)
print(solve(64, (x,y)))

def solve2(steps: int, start:tuple[int,int]) -> int:
    current = set([start])
    for i in range(steps):
        next = []
        for p in current:
            xx, yy = p
            l = (xx-1, yy)
            u = (xx, yy-1)
            r = (xx+1, yy)
            d = (xx, yy+1)
            next.extend([p for p in [l, u, r, d]
                    if lines[p[1]%height][p[0]%width]!="#"])
        current = set(next)
    return len(current)

steps = 26501365
x0 = solve2(steps%width, (x,y))
x1 = solve2(steps%width + width, (x,y))
x2 = solve2(steps%width + 2 * width, (x,y))
firstDiff = x1-x0
secondDiff = (x2-x1) - (x1-x0)
a = secondDiff//2
b = firstDiff - 3*a
c = x0 - a - b

n = steps // width + 1
print(a*n**2+b*n+c)

# 620962518745459