from dataclasses import dataclass
from functools import cache
from pprint import pprint


@dataclass
class Brick:
    x1: int
    y1: int
    z1: int
    x2: int
    y2: int
    z2: int    
    
    def may_support(self, other: "Brick") -> bool:
        return (not (other.x2 < self.x1
                or self.x2 < other.x1)
                and
                not (other.y2 < self.y1
                or self.y2 < other.y1)
                and self.z2<other.z1 and self!=other)

    def supports(self, other: "Brick") -> bool:
        return self.may_support(other) and self.z2+1==other.z1
    
    def drop(self, steps: int):
        self.z1 -= steps
        self.z2 -= steps


def parse_line(line: str) -> Brick:
    x1, y1, z1, x2, y2, z2 = [x
                              for y in line.split("~")
                              for x in y.split(",")]
    
    return Brick(int(x1), int(y1), int(z1), 
                 int(x2), int(y2), int(z2))

def read_file() -> list[str]:
    with open("input22.txt") as f:
        lines = [x.strip() for x in f.readlines()]
        return lines


lines = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9""".split("\n")

lines = read_file()
bricks = [parse_line(line) for line in lines]
# Sort so that bottom block is always moved down first
bricks.sort(key=lambda b: b.z1)
for i, brick in enumerate(bricks):
    bricks_below = [b for b in bricks if b.may_support(brick)]
    steps = brick.z1 - 1
    if any(bricks_below):
        z = max([b.z2 for b in bricks_below])
        steps = brick.z1 - z - 1
    brick.drop(steps)

supported_by: dict[int,set[int]] = dict()
supports: dict[int,set[int]] = dict()
for i, brick in enumerate(bricks):
    supported_bricks = [j for j,b in enumerate(bricks)
                        if brick.supports(b)]
    supports[i] = set(supported_bricks)
    for s in supported_bricks:
        if not s in supported_by:
            supported_by[s] = set()
        supported_by[s].add(i)

res = 0
for i, other in supports.items():
    if all([len(supported_by[j])>1 for j in other]):
        res += 1

print(res)

res = 0
for i in range(len(bricks)):
    disintegrated_blocks = set()
    working_set = set([i])
    while len(working_set)>0:
        # Distintegrate blocks
        disintegrated_blocks.update(working_set)
        dropped = set()
        for j in working_set:
            dropped.update([b 
                            for b in supports[j] 
                            if len(supported_by[b].difference(disintegrated_blocks))==0])
        working_set = dropped
        
    res += len(disintegrated_blocks)-1
    
print(res)