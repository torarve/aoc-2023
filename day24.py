from itertools import combinations
import re

import sympy


def read_file() -> list[str]:
    with open("input24.txt") as f:
        lines = [x.strip() for x in f.readlines()]
        return lines

lines = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3""".split("\n")

def parse(line: str) -> str:
    e = re.findall("(-?\d+)", line)
    px, py, pz, vx, vy, vz = tuple([int(x) for x in e])
    return px, py, pz, vx, vy, vz


# bounds = (7, 27)
bounds = (200000000000000, 400000000000000)
lines = read_file()

paths = [parse(line) for line in lines]
count = 0
for p1, p2 in combinations(paths, 2):
    a = p1[3]
    b = -p2[3]
    c = p1[4]
    d = -p2[4]
    det = a*d - b*c
    if det == 0:
        continue
    
    e = p2[0] - p1[0]
    f = p2[1] - p1[1]    
    t1 = (d*e -b*f)/det
    t2 = (-c*e + a*f)/det
    if t1<0 or t2 < 0:
        continue
    x = p1[0] + t1*p1[3]
    y = p1[1] + t1*p1[4]
    if not (bounds[0]<=x and x<=bounds[1]):
        continue
    if not (bounds[0]<=y and y<=bounds[1]):
        continue

    count += 1
    
print(count)

x, y, z, dx, dy, dz = sympy.symbols("x y z dx dy dz")

equations = []
symbols = [x, y, z, dx, dy, dz]
for i, p in enumerate(paths):
    t = sympy.symbols(f"t{i}")
    symbols.append(t)
    x1, y1, z1, dx1, dy1, dz1 = p
    equations.extend([
        sympy.Eq(x+t*dx, x1+t*dx1),
        sympy.Eq(y+t*dy, y1+t*dy1),
        sympy.Eq(z+t*dz, z1+t*dz1)       
    ])

# Only need three equations
c = 3
res = sympy.solve(equations[:c*3], *symbols[:6+c])
x, y, z, dx, dy, dz = [x for x in res][0][:6]
print(x+y+z)