from dataclasses import dataclass
from pprint import pprint


def read_file() -> list[str]:
    with open("input15.txt") as f:
        lines = [x.strip() for x in f.readlines()]
        return lines

lines = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7""".split("\n")
lines = read_file()

@dataclass
class Lens:
    label: str
    value: int
    
    def __hash__(self) -> int:
        return hash(self.label)


def do_hash(input: str) -> int:
    value = 0
    for c in input:
        value = ((value + ord(c)) * 17) % 256
    return value

        
result = 0
for line in lines:
    result += sum([do_hash(x) for x in line.split(",")])

print(result)

def operations(lines: list[str]) -> tuple[str,int]:
    for line in lines:
        for op in line.split(","):
            if op.endswith("-"): yield (op[:-1], None)
            if "=" in op:
                label, value = tuple(op.split("="))
                yield label, int(value)
    
boxes = list([[] for x in range(256)])

for label, value in operations(lines):
    idx = do_hash(label)
    if value is not None:
        found = False
        for i in range(len(boxes[idx])):
            if boxes[idx][i].label == label:
                boxes[idx][i].value = value
                found = True
                
        if not found:
            boxes[idx].append(Lens(label, value))
    else:
        boxes[idx] = [x for x in boxes[idx] if x.label!=label]

result = 0
for i, box in enumerate(boxes):
    for j, lens in enumerate(box):
        result += (i+1)*(j+1)*lens.value
        
print(result)