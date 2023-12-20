from dataclasses import dataclass, field
from math import lcm
from pprint import pprint
from queue import Queue


def read_file() -> list[str]:
    with open("input20.txt") as f:
        lines = [x.strip() for x in f.readlines()]
        return lines


lines = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a""".split("\n")


lines = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output""".split("\n")
# print(lines)

lines =read_file()

@dataclass
class Bus:
    modules: dict = field(default_factory=dict)
    queue: Queue[tuple[str, str, bool]] = field(default_factory=Queue)
    count_low: int = 0
    count_high: int = 0
    signals = []
    
    def send(self, targets: list[str], source: str, pulse: bool):
        self.signals = []
        self.send_to(targets, source, False)
        self._process_queue()
        
    
    def button_press(self):
        self.signals = []
        self.send_to(["broadcaster"], "button", False)
        self._process_queue()
         
    def _process_queue(self):
        while not self.queue.empty():
            target, source, pulse = self.queue.get()
            if pulse:
                self.count_high += 1
            else:
                self.count_low += 1
            if target in self.modules:
                self.modules[target].signal(source, pulse)
            
    def send_to(self, targets: list[str], source: str, pulse: bool):
        for target in targets:
            self.signals.append((source, target, pulse))
            self.queue.put((target, source, pulse))


@dataclass
class FlipFlop:
    name: str
    state: bool = False
    outputs: list[str] = field(default_factory=list)
    bus: Bus = field(default=None, repr=False)
    
    def signal(self, source, signal: bool):
        if not signal: # Low signal
            self.state = not self.state
            self.bus.send_to(self.outputs, self.name, self.state)

@dataclass
class Conjunction:
    name: str
    inputs: dict[str, bool] = field(default_factory=dict)
    outputs: list[str] = field(default_factory=list)
    bus: Bus = field(default=None, repr=False)
    
    @property
    def state(self):
        return ";".join([f"{name}={value}" for name,value in self.inputs.items()])

    @property
    def pulse(self):
        return not all(self.inputs.values())

    def signal(self, source, signal: bool):
        self.inputs[source] = signal
        pulse = not all(self.inputs.values())
        self.bus.send_to(self.outputs, self.name, pulse)
    
@dataclass
class Broadcaster:
    name: str = "broadcaster"
    outputs: list[str] = field(default_factory=list)
    bus: Bus = field(default=None, repr=False)

    def signal(self, source, pulse: bool):
        self.bus.send_to(self.outputs, self.name, pulse)


class Builder:
    
    def __init__(self):
        self._blueprints: dict[str, tuple[str, list, type]] = {}
        self._sources: dict[str, list[str]] = {}

    
    def parse_line(self, line: str):
        i = line.index(" -> ")
        name = line[0:i]
        outputs = line[i+len(" -> "):].split(", ")
        if name[0]=="&":
            module_type = Conjunction
            name = name[1:]
        elif name[0] == "%":
            module_type = FlipFlop
            name = name[1:]
        else:
            module_type = Broadcaster
        
        self._blueprints[name] = name, outputs, module_type
        for target in outputs:
            t = self._sources.get(target, [])
            t.append(name)
            self._sources[target] = t
    
    def parse(self, lines: list[str]):
        for line in lines:
            builder.parse_line(line)            
        
    def build(self):
        bus = Bus()
        for name, outputs, module_type in self._blueprints.values():
            kwargs = { "name" : name, "bus": bus, "outputs": outputs }
            if module_type == Conjunction:
                input_names = self._sources.get(name, [])
                kwargs["inputs"] = dict([(x, False) for x in input_names])
                
            bus.modules[name] = module_type(**kwargs)
            
        return bus
    

def make_subgraph(bus: Bus, start: str) -> list[FlipFlop|Conjunction]:
    subgraph = []
    working_set = [bus.modules[start]]
    visited = set()
    while working_set:
        subgraph.extend(working_set)
        visited.update([x.name for x in working_set])
        outputs = [x.outputs for x in working_set]
        temp = []
        for o in outputs:
            temp.extend([bus.modules[x] for x in o if x!="rg" and x not in visited])
        working_set = temp
        
    return subgraph


def check_subgraph(bus: Bus, name, subgraph):
    def subgraph_state(graph):
        return hash(":".join([str(g.state) for g in graph]))
    
    c = 0
    seen = set([subgraph_state(subgraph)])
    while True:
        bus.send([name], "broadcaster", False)
        c+=1
        s = subgraph_state(subgraph)
        t = [value for _, target, value in bus.signals if target == "rg"]
        if any(t):
            return c
        if s in seen:
            return 0
        seen.add(s)
    

builder = Builder()
builder.parse(lines)
bus = builder.build()

for i in range(1000):
    bus.button_press()
print(bus.count_low*bus.count_high)

bus = builder.build()
broadcaster: Broadcaster = bus.modules["broadcaster"]
values = []
for name in broadcaster.outputs:
    subgraph = make_subgraph(bus, name)
    values.append(check_subgraph(bus, name, subgraph))

print(lcm(*values))
