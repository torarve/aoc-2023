from itertools import combinations
import re
import matplotlib.pyplot as plt
import networkx as nx


def read_file() -> list[str]:
    with open("input25.txt") as f:
        lines = [x.strip() for x in f.readlines()]
        return lines

lines = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr""".split("\n")

lines = read_file()
    
G = nx.Graph()
adjacency: dict[str,list[str]] = {}
nodes: set[str] = set()
for line in lines:
    m = re.findall(r"\w+", line)
    nodes.update(m)
    adjacency[m[0]] = m[1:]


G.add_nodes_from(nodes)
for k in adjacency:
    for v in adjacency[k]:
        G.add_edge(k, v, capacity=1)

# nx.draw(G)
# plt.show()
for s, t in combinations(list(G.nodes), 2):
    n, g = nx.minimum_cut(G, s, t)
    if n == 3:
        print(len(g[0])*len(g[1]))
        break

