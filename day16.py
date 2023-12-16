from dataclasses import dataclass
from pprint import pprint


def read_file() -> list[str]:
    with open("input16.txt") as f:
        lines = [x.strip() for x in f.readlines()]
        return lines


class Matrix:
    def __init__(self, data: str, width: int, height: int):
        self.height = height
        self.width = width
        self.data = [x for x in data]
        
    def __hash__(self):
        return hash("".join(self.data))
    
    def __getitem__(self, pos):
        x, y = pos
        return self.data[y*self.width + x]
    
    def __setitem__(self, pos, value):
        x, y = pos
        self.data[y*self.width + x] = value

    def rows(self):
        for i in range(self.height):
            yield self.data[i*self.width:(i+1)*self.width]
            
    def row(self, y):
        return self.data[y*self.width:(y+1)*self.width]

    def __str__(self):
        return "\n".join(["".join(row) for row in self.rows()])
            
lines = """.|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|....""".split("\n")

lines = read_file()

@dataclass
class Beam:
    direction: str
    position: tuple[int, int]
    
    def step(self):
        x, y = self.position
        match self.direction:
            case "e": x+=1
            case "w": x+=-1
            case "n": y-=1
            case "s": y+=1
            
        self.position = (x,y)
        return self
    
    def within_range(self, w, h):
        x, y = self.position
        return x>=0 and x<w and y>=0 and y<h
    
    def __hash__(self) -> int:
        return hash(f"{self.direction}:{self.position[0]}:{self.position[1]}")
        
width = len(lines[0])
height = len(lines)
m = Matrix("".join(lines), width, height)

def get_energized_count(m: Matrix, start: Beam):
    paths = Matrix(["."]*m.width*m.height, m.width, m.height)        
    traced: set[Beam] = set()
    beams = [start]
    while len(beams):
        temp = []
        for beam in beams:
            paths[beam.position] = "#"
            traced.add(beam)
            x, y = beam.position
            match m[beam.position]:
                case ".":
                    temp.append(beam.step())
                case "|":
                    if beam.direction in ("n", "s"):
                        temp.append(beam.step())
                    else:
                        temp.append(Beam("n", (x, y-1)))
                        temp.append(Beam("s", (x, y+1)))
                case "-":
                    if beam.direction in ("w", "e"):
                        temp.append(beam.step())
                    else:
                        temp.append(Beam("w", (x-1, y)))
                        temp.append(Beam("e", (x+1, y)))
                case "/":
                    match beam.direction:
                        case "e": temp.append(Beam("n", (x, y-1)))
                        case "w": temp.append(Beam("s", (x, y+1)))
                        case "n": temp.append(Beam("e", (x+1, y)))
                        case "s": temp.append(Beam("w", (x-1, y)))
                case "\\":
                    match beam.direction:
                        case "e": temp.append(Beam("s", (x, y+1)))
                        case "w": temp.append(Beam("n", (x, y-1)))
                        case "n": temp.append(Beam("w", (x-1, y)))
                        case "s": temp.append(Beam("e", (x+1, y)))
                    
        beams = [x for x in temp 
                if x.within_range(m.width, m.height)
                and x not in traced]
    
    return len([x for x in paths.data if x=="#"])
    
print(get_energized_count(m, Beam("e", (0,0))))

max_count = 0
for row in range(m.height):
    max_count = max(max_count, get_energized_count(m, Beam("e", (0,row))))
    max_count = max(max_count, get_energized_count(m, Beam("w", (m.width-1,row))))
for col in range(m.width):
    max_count = max(max_count, get_energized_count(m, Beam("s", (col, 0))))
    max_count = max(max_count, get_energized_count(m, Beam("n", (col, m.height-1))))
    
print(max_count)