from dataclasses import dataclass, field
from queue import PriorityQueue


def read_file() -> list[str]:
    with open("input17.txt") as f:
        lines = [x.strip() for x in f.readlines()]
        return lines

lines = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533""".split("\n")

lines = read_file()

height = len(lines)
width = len(lines[0])

@dataclass
class Node:
    x: int
    y: int
    dx: int
    dy: int
    s: int
    
    @property
    def key(self) -> int:
        return f"{self.x}:{self.y}:{self.dx}:{self.dy}:{self.s}"
    
    def __hash__(self) -> int:
        return hash(self.key)    
    
    def neighbours(self, lo: int, hi: int):
        if lo<=self.s and self.s<=hi:
            yield self.turn_right()
        if self.s<hi:
            yield Node(self.x+self.dx, self.y+self.dy, self.dx, self.dy, self.s+1)
        if lo<=self.s and self.s<=hi:
            yield self.turn_left()
        
    def turn_left(self):
        dx, dy = self.dy, -self.dx
        return Node(self.x+dx, self.y+dy, dx, dy, 1)

    def turn_right(self):
        dx, dy = -self.dy, self.dx
        return Node(self.x+dx, self.y+dy, dx, dy, 1)

@dataclass(order = True)
class QueueItem:
    priority: int
    node: Node = field(compare=False)
    
def run(lo: int = 1, hi: int = 3):
    distance: dict[Node, int] = {}
    distance[Node(1,0,1,0,1)] = int(lines[0][1])
    distance[Node(0,1,0,1,1)] = int(lines[1][0])
    visited = set()
    q: PriorityQueue[QueueItem] = PriorityQueue()
    q.put(QueueItem(int(lines[0][1]), Node(1,0,1,0,1)))
    q.put(QueueItem(int(lines[1][0]), Node(0,1,0,1,1)))
    while True:
        t = q.get()
        current, current_distance = t.node, t.priority
                
        neighbours = [n for n in current.neighbours(lo, hi) 
                if 0<=n.x and n.x<width and 0<=n.y and n.y<height]
        for n in neighbours:
            w = int(lines[n.y][n.x])
            d = current_distance + w
            if n not in distance or distance[n]>d:
                q.put(QueueItem(d, n))
                distance[n] = d
            if n.x == width-1 and n.y==height-1:
                return d
        visited.add(current)

print(run())
print(run(4,10))