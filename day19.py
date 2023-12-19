from dataclasses import dataclass
from functools import reduce
from itertools import accumulate
from operator import mul
from pprint import pprint
import re


def read_file() -> list[str]:
    with open("input19.txt") as f:
        lines = [x.strip() for x in f.readlines()]
        return lines



lines = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}""".split("\n")

lines =read_file()

@dataclass()
class Part:
    x: int = 0
    m: int = 0
    a: int = 0
    s: int = 0
    
    @property
    def total_rating(self):
        return self.x + self.m + self.a + self.s

@dataclass
class Rule:
    category: str
    op: str
    value: int
    result: str
    
    def matches(self, part: Part) -> bool:
        v = getattr(part, self.category)
        match self.op:
            case "<": return v < self.value
            case ">": return v > self.value
        raise("Invalid")
    
    def range_matched(self):
        match self.op:
            case "<": return (1, self.value-1)
            case ">": return (self.value+1, 1)
        raise("Invalid")

@dataclass
class Workflow:
    name: str
    rules: list[Rule]
    default: str
    
    def evaluate(self, part: Part):
        for rule in self.rules:
            if rule.matches(part):
                return rule.result
        return self.default

def parse_part(p: str) -> Part:
    kwargs = {}
    parts = p[1:-1].split(",")
    for n, v in [(x[0], int(x[2:])) for x in parts]:
        kwargs[n] = v
        
    return Part(**kwargs)
    

def parse_rule(r: str) -> Rule:
    tmp = re.match("^(.+)([<>])(\d+):(.+)", r)
    category, op, value, result = tmp.groups()
    return Rule(category, op, int(value), result)


def parse_workflow(l: str) -> Workflow:
    i = l.index("{")
    name = l[:i]
    tmp = l[i+1:-1].split(",")
    default = tmp.pop()
    rules = [parse_rule(r) for r in tmp]
    return Workflow(name, rules, default)


# Parse workflows
workflows: dict[str,Workflow] = {}
for i in range(len(lines)):
    line = lines[i]
    if line == "": break
    w = parse_workflow(line)
    workflows[w.name] = w


# Parse ratings
parts: list[Part] = []
for i in range(i+1, len(lines)):
    line = lines[i]
    parts.append(parse_part(line))
    

def evaluate(workflows: dict[str, Workflow], part: Part) -> int:
    current = "in"
    while current not in ["A", "R"]:
        w = workflows[current]
        current = w.evaluate(part)
    
    # print(current)
    if current=="R":
        return 0
    
    # print(part.total_rating)
    return part.total_rating
    
result1 = 0
for part in parts:
    result1 += evaluate(workflows, part)
print(result1)

def not_implemented(): raise "Not implemented"

working_set: list[tuple[int, dict[str,tuple[int,int]]]] = [
    ("in", { "x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000) })]
accepted = []
rejected = []
while working_set:
    output = []
    for name, xmas in working_set:
        w = workflows[name]
        for rule in w.rules:
            l, h = xmas[rule.category]
            match rule.op:
                case "<":
                    if h < rule.value:
                        # All values lower (all match)
                        not_implemented()
                    elif rule.value <= l:
                        # All values are higher (no match)
                        pass
                    else:
                        # Need to split
                        new_xmas = dict(xmas.items())
                        new_xmas[rule.category] = l, rule.value-1
                        assert xmas[rule.category] != new_xmas[rule.category]
                        output.append((rule.result, new_xmas))
                        
                        xmas[rule.category] = rule.value, h
                case ">":
                    if l > rule.value:
                        # All values higher (all match)
                        not_implemented()
                    elif h <= rule.value:
                        # All values lower (no match)
                        pass
                    else:
                        # Need to split
                        new_xmas = dict(xmas.items())
                        new_xmas[rule.category] = rule.value+1, h
                        output.append((rule.result, new_xmas))
                        
                        xmas[rule.category] = l, rule.value
                        
        output.append((w.default, xmas))

    accepted.extend([x[1] for x in output if x[0] == "A"])
    rejected.extend([x[1] for x in output if x[0] == "R"])
    working_set = [x for x in output if x[0] not in ["A", "R"]]

result2 = sum([
    reduce(mul, [h-l+1 for l,h in d.values()]) 
    for d in accepted])
print(result2)
