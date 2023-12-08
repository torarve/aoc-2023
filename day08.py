from functools import reduce
from math import gcd, lcm
from operator import mul
import re


def read_file() -> list[str]:
    with open("input08.txt") as f:
        lines = [x.strip() for x in f.readlines()]
        return lines


lines = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)""".split("\n")

lines = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)""".split("\n")

lines = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)""".split("\n")

lines = read_file()

def parse_line(line: str) -> tuple[str,str]:
    key = line[0:3]
    left = line[7:10]
    right = line[12:15]
    return (key, (left,right))

instructions = lines[0]
adjacency = dict([parse_line(line) for line in lines[2:]])

steps = 0
current = 'AAA'
while current!='ZZZ':
    i = 1 if instructions[steps%len(instructions)]=='R' else 0
    current = adjacency[current][i]
    steps += 1
    
print(steps)


all_steps = []
for current in [x for x in adjacency.keys() if x.endswith("A")]:
    steps = 0
    seen = False
    while not current.endswith("Z"):
        i = 1 if instructions[steps%len(instructions)]=='R' else 0
        current = adjacency[current][i]
        steps += 1
    all_steps.append(steps)
    
print(lcm(*all_steps))
