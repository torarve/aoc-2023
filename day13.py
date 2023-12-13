def read_file() -> list[str]:
    with open("input13.txt") as f:
        lines = [x.strip() for x in f.readlines()]
        return lines

class Matrix:
    def __init__(self, data: str, width: int, height: int):
        self.height = height
        self.width = width
        self.data = data
        
    @staticmethod
    def from_list(data: list[str]) -> "Matrix":
        h = len(data)
        w = len(data[0])
        return Matrix("".join(data), w, h)
    
    def rows(self):
        for i in range(self.height):
            yield self.data[i*self.width:(i+1)*self.width]
            
    def columns(self):
        for i in range(self.width):
            yield self.data[i::self.width]

    def find_reflection_lines(self):
        lines = []
        for i in range(1, self.width):
            if self.reflects_vertically(i):
                lines.append((i, 0))
        for i in range(1, self.height):
            if self.reflects_horizontally(i):
                lines.append((0, i))
        return lines
        
    def find_reflection_line(self):
        for i in range(1, self.width):
            if self.reflects_vertically(i):
                return (i, 0)
        for i in range(1, self.height):
            if self.reflects_horizontally(i):
                return (0, i)
        return (0, 0)
    
    def reflects_vertically(self, col):
        if col == 0 or col == self.width:
            return False
        for row in self.rows():
            lhs, rhs = row[:col], row[col:]
            length = min(len(lhs), len(rhs))
            lhs = lhs[len(lhs)-length:]
            rhs = rhs[:length]
            rhs = rhs[::-1]
            if lhs != rhs:
                return False
            
        return True
    
    def reflects_horizontally(self, row):
        if row == 0 or row == self.height:
            return False
        for column in self.columns():
            lhs, rhs = column[:row], column[row:]
            length = min(len(lhs), len(rhs))
            lhs = lhs[len(lhs)-length:]
            rhs = rhs[:length]
            rhs = rhs[::-1]
            if lhs != rhs:
                return False
            
        return True

        
def parse_patterns(lines: list[str]) -> list[Matrix]:
    patterns = []
    current = []
    for line in lines:
        if line == "":
            patterns.append(Matrix.from_list(current))
            current = []
        else:
            current.append(line)

    patterns.append(Matrix.from_list(current))
    return patterns

    
lines = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""".split("\n")

lines = read_file()

patterns = parse_patterns(lines)

cols, rows = 0, 0
for j, pattern in enumerate(patterns):
    x, y = pattern.find_reflection_line()
    cols, rows = cols+x, rows+y
print(rows*100 + cols)

cols, rows = 0, 0
for j, pattern in enumerate(patterns):
    org = pattern.find_reflection_line()
    data = pattern.data
    for i in range(len(data)):
        c = "." if data[i] == "#" else "#"
        m = Matrix(data[:i]+c+data[i+1:], pattern.width, pattern.height)
        reflections = set(m.find_reflection_lines())
        if org in reflections:
            reflections.remove(org)
        if len(reflections)==1:
            x, y = list(reflections)[0]
            cols, rows = cols+x, rows+y
            break

print(rows*100+cols)