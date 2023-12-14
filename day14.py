def read_file() -> list[str]:
    with open("input14.txt") as f:
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
        
    def move_up(self, col, row):
        if row == 0:
            return
        if self[col, row] != "O":
            print(self[col, row])
            raise "Not rounded rock!"
        
        while row>0 and self[col, row-1] == ".":
            self[col, row] = "."
            self[col, row-1] = "O"
            row -= 1
            
    def move_down(self, col, row):
        if row == self.height-1:
            return
        if self[col, row] != "O":
            print(self[col, row])
            raise "Not rounded rock!"
        
        while row<self.height-1 and self[col, row+1] == ".":
            self[col, row] = "."
            self[col, row+1] = "O"
            row += 1
            
    def move_left(self, col, row):
        if col == 0:
            return
        if self[col, row] != "O":
            print(self[col, row])
            raise "Not rounded rock!"
        
        while col>0 and self[col-1, row] == ".":
            self[col, row] = "."
            self[col-1, row] = "O"
            col -= 1
    
    def move_right(self, col, row):
        if col == self.width-1:
            return
        if self[col, row] != "O":
            print(self[col, row])
            raise "Not rounded rock!"
        
        while col<self.width-1 and self[col+1, row] == ".":
            self[col, row] = "."
            self[col+1, row] = "O"
            col += 1
    
    def spin(self):
        for r in range(m.height):
            for c in range(m.width):
                if m[c,r] == "O":
                    m.move_up(c,r)
        for c in range(m.width):
            for r in range(m.height):
                if m[c,r] == "O":
                    m.move_left(c,r)
        for r in reversed(range(m.height)):
            for c in range(m.width):
                if m[c,r] == "O":
                    m.move_down(c,r)
        for c in reversed(range(m.width)):
            for r in range(m.height):
                if m[c,r] == "O":
                    m.move_right(c,r)

    def rows(self):
        for i in range(self.height):
            yield self.data[i*self.width:(i+1)*self.width]
            
    def row(self, y):
        return self.data[y*self.width:(y+1)*self.width]

    def __str__(self):
        return "\n".join(self.rows())
    
    def calculate_load(self):
        load = 0
        for i in range(self.height):
            number_of_rocks = len([x for x in self.row(i) if x=="O"])
            # print(i, number_of_rocks)
            load += (self.height-i) * number_of_rocks
            
        return load

lines = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""".split("\n")

# print(lines)

lines = read_file()

width = len(lines[0])
height = len(lines)
m = Matrix("".join(lines), width, height)

for r in range(m.height):
    for c in range(m.width):
        if m[c,r] == "O":
            m.move_up(c,r)
            
print(m.calculate_load())

states = {}
i = 0
while i<1000000000:
    m.spin()
    h = hash(m)
    if h in states.keys():
        cycle_count = i-states[h]
        tail = i-states[h]        
        x = (1000000000 - i)//cycle_count
        i += x*cycle_count
        while i+cycle_count<1000000000:
            i += cycle_count
    states[h] = i
    i += 1

print(m.calculate_load())
