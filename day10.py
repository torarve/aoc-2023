from typing import Any


def read_file() -> list[str]:
    with open("input10.txt") as f:
        lines = [x.strip() for x in f.readlines()]
        return lines

class Matrix:
    def __init__(self, height, width):
        self._values: list = [None]*height*width
        self._height = height
        self._width = width

    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height

    def __getitem__(self, pos):
        row, col = pos
        return self._values[row*self._width + col]
    
    def __setitem__(self, pos, value):
        row, col = pos
        self._values[row*self._width + col] = value
        
    def find_value(self, value):
        pos = self._values.index(value)
        row = pos // self._width
        col = pos % self._width
        return row, col
    
    def get_surrounding(self, row, col):
        left = self[row,col-1] if col>0 else None
        above = self[row-1, col] if row>0 else None
        right = self[row, col+1] if col<self._width-1 else None
        below = self[row+1, col] if row<self._height-1 else None
        return left, above, right, below
    
    def within_bounds(self, row, col):
        return (
            row>=0 and row<=self.height-1
            and col>=0 and col<=self.width-1)
        
    def fill_empty(self, row, col, value):
        working_set = [(row, col)]
        while len(working_set):
            r, c = working_set.pop()
            if self[r, c] is None:
                self[r, c] = value
                if r>0: working_set.append((r-1, c))
                if r<self.height-1: working_set.append((r+1,c))
                if c>0: working_set.append((r, c-1))
                if c<self.width-1: working_set.append((r, c+1))
                
    def count(self, value):
        return len([x for x in self._values if x == value])

lines = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF""".split("\n")

lines = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...""".split("\n")

lines = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L""".split("\n")

lines = read_file()

map = Matrix(len(lines), len(lines[0]))
for r, line in enumerate(lines):
    for c, val in enumerate(line):
        map[r,c] = val
    
start = map.find_value("S")

# step 1: find starting pipe
left, top, right, bottom = map.get_surrounding(*start)

if left!="-" and left!="L" and left!="F":
    left = None
if top!="|" and top!="7" and top!="F":
    top = None
if right!="-" and right!="7" and right!="J":
    right = None
if bottom!="|" and bottom!="L" and bottom!="J":
    bottom = None

start_pipe = None
if left and top: start_pipe = "J"
if left and right: start_pipe = "-"
if left and bottom: start_pipe = "7"
if top and right: start_pipe = "L"
if top and bottom: start_pipe = "|"
if right and bottom: start_pipe = "F"

map[start] = start_pipe

neighbours = {
    "|": [(-1,0), (1,0)],
    "-": [(0,-1), (0,1)],
    "L": [(-1,0), (0,1)],
    "J": [(-1,0), (0,-1)],
    "7": [(-1,0), (1,0)],
    "F": [(1,0), (0,1)]
}

def get_start_direction():
    match start_pipe:
        case "|": return [(-1, 0), (1, 0)]
        case "-": return [(0, -1), (0, 1)]
        case "L": return [(-1, 0), (0, 1)]
        case "J": return [(-1, 0), (0, -1)]
        case "7": return [(1, 0), (0,-1)]
        case "F": return [(1, 0), (0, 1)]

def new_direction(current, pipe):
    if pipe == "|" or pipe == "-":
        return current
    
    if pipe == "L" and current == (1, 0):
        return (0,1)
    elif pipe == "L" and current == (0, -1):
        return (-1, 0)
    
    if pipe == "J" and current == (1, 0):
        return (0, -1)
    elif pipe == "J" and current == (0, 1):
        return (-1, 0)
    
    if pipe == "7" and current == (0, 1):
        return (1, 0)
    elif pipe == "7" and current == (-1, 0):
        return (0, -1)
    
    if pipe == "F" and current == (0, -1):
        return (1, 0)
    elif pipe == "F" and current == (-1, 0):
        return (0, 1)
    
    raise "Not possible"

direction = get_start_direction()
position = [start, start]

distance = Matrix(len(lines), len(lines[0]))
distance[start] = 0
done = False
max_distance = 0
while not done:
    for i in range(2):
        d = direction[i]
        p = position[i]
        next_pos = p[0] + d[0], p[1] + d[1]
        if distance[next_pos] is not None:
            done = True
        else:
            distance[next_pos] = distance[p] + 1
            position[i] = next_pos
            direction[i] = new_direction(d, map[next_pos])
        max_distance = max(distance[next_pos], max_distance)
        
print(max_distance)

def get_left(pos):
    match pos:
        case (1,0): return (0,1)
        case (-1,0): return (0,-1)
        case (0,1): return (-1,0)
        case (0,-1): return (1,0)
    
    raise "Not possible"


pos = start
direction = get_start_direction()[1]
done = False
inside = "L"


while not done:
    d = direction
    next_pos = pos[0] + d[0], pos[1] + d[1]
    p = next_pos
    ly, lx = get_left(direction)
    if distance.within_bounds(p[0]+ly, p[1]+lx):
        if distance[p[0]+ly, p[1]+lx] is None:
            distance.fill_empty(p[0]+ly, p[1]+lx, "L")
    else:
        inside = None
    
    direction = new_direction(d, map[next_pos])
    ly, lx = get_left(direction)
    if distance.within_bounds(p[0]+ly, p[1]+lx):
        if distance[p[0]+ly, p[1]+lx] is None:
            distance.fill_empty(p[0]+ly, p[1]+lx, "L")
    else:
        inside = None

    if next_pos == start:
        done = True
    pos = next_pos

for row in range(map.height):
    tmp = ""
    for col in range(map.width):
        if type(distance[row, col]) == int:
            tmp += map[row,col]
        else:
            tmp += "I" if distance[row, col] == inside else " "
    print(tmp)
    
print(distance.count(inside))