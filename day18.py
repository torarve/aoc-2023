from dataclasses import dataclass
from pprint import pprint


def parse_line(line: str) -> tuple[str,int]:
    a, b, c = line.split(" ")
    return a, int(b)

def read_file() -> list[tuple[str, int]]:
    with open("input18.txt") as f:
        lines = [parse_line(x.strip()) for x in f.readlines()]
        return lines

class Matrix:
    def __init__(self, width: int, height: int):
        self.height = height
        self.width = width
        self.data = [None] * width*height
        
    def __hash__(self):
        return hash("".join(self.data))
    
    def __getitem__(self, pos):
        x, y = pos
        return self.data[y*self.width + x]
    
    def __setitem__(self, pos, value):
        x, y = pos
        if y>self.height-1:
            raise "Error"
        if x>self.width-1:
            raise "Error"
        self.data[y*self.width + x] = value

    def rows(self):
        for i in range(self.height):
            yield self.data[i*self.width:(i+1)*self.width]
            
    def row(self, y):
        return self.data[y*self.width:(y+1)*self.width]
    
    def fill_empty(self, ix, iy, value):
        working_set = [(ix, iy)]
        while len(working_set):
            x, y = working_set.pop()
            if self[x,y] is None:
                self[x,y] = value
                if y>0: working_set.append((x, y-1))
                if y<self.height-1: working_set.append((x, y+1))
                if x>0: working_set.append((x-1,y))
                if x<self.width-1: working_set.append((x+1,y))

    def non_empty_count(self) -> int:
        return len([x for x in self.data if x is not None])

    def __str__(self):
        return "\n".join(["".join([x if x is not None else "." for x in row]) for row in self.rows()])

lines = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)""".split("\n")

lines = [parse_line(l) for l in lines]
# lines = read_file()

# Walk!

def find_bounds(lines: list[tuple[str,int]]) -> tuple[int, int, int, int]:
    x, y = 0, 0
    min_x, max_x = 0, 0
    min_y, max_y = 0, 0
    for d, l in lines:
        for i in range(l):
            match d:
                case "L": x -= 1
                case "U": y -= 1
                case "D": y += 1
                case "R": x += 1
                
            min_x, max_x = min(x, min_x), max(x, max_x)
            min_y, max_y = min(y, min_y), max(y, max_y)

    w = max_x-min_x+1
    h = max_y-min_y+1
    return w, h, -min_x, -min_y

w, h, ix, iy = find_bounds(lines)
m = Matrix(w, h)

x, y = ix, iy

for d, l in lines:
    for i in range(l):
        m[x,y] = "#"
        match d:
            case "L": x -= 1
            case "U": y -= 1
            case "D": y += 1
            case "R": x += 1
            
        if x<0 or y<0:
            raise "Error"

m.fill_empty(ix+1, iy+1, "#")
print(m.non_empty_count())

@dataclass
class Line:
    x1: int
    y1: int
    x2: int
    y2: int
    
    def check(self, y: int) -> bool:
        y1, y2 = self.y1, self.y2
        if y1>y2:
            y1, y2 = y2, y1
            
        return y1 <= y and y <= y2
    
polygon: list[Line] = []
x,y = ix, iy
print(x,y)
for d, l in lines:
    match d:
        case "L": 
            polygon.append(Line(x, y, x-l, y))
            x, y = x-l-1, y
        case "U": 
            polygon.append(Line(x, y, x, y-l))
            x, y = x, y-l-1
        case "D": 
            polygon.append(Line(x, y, x, y+l))
            x, y = x, y+l+1
        case "R": 
            polygon.append(Line(x, y, x+l, y))
            x, y = x+l+1, y
    t = polygon[-1]
    # print(t)
    x, y = t.x2, t.y2
    

# pprint(polygon)
for y in range(-iy, h-iy+1):
    count = 0
    for l in [x for x in polygon if x.check(y)]:
        if l.y1==l.y2:
            count += abs(l.x2 - l.x1)
        else:
            count += 1
        # print(l, count)
            
    print(count)
            
    # print(y)
    
# print(m)