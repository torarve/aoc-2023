from pprint import pprint
import queue
import sys


sys.setrecursionlimit(100000)

def read_file() -> list[str]:
    with open("input23.txt") as f:
        lines = [x.strip() for x in f.readlines()]
        return lines

lines = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#""".split("\n")

lines = read_file()

def next_steps(x,y):
    return [
        (x-1, y),
        (x+1, y),
        (x, y-1),
        (x, y+1)
    ]

width = len(lines[0])
height = len(lines)

def visit(x, y, path: set, slopes: bool = True):
    if y+1 == height:
        # for i in range(len(lines)):
        #     tmp = [x for x in lines[i]]
        #     for j in range(len(lines[0])):
        #         tmp[j] = "O" if (j,i) in path else lines[i][j]
        #     print("".join(tmp))
        return len(path)
    
    if slopes == False or lines[y][x] == ".":
        next = [(xx,yy) for xx,yy in next_steps(x,y) 
                if 0<xx and xx<width and 0<yy and yy<height
                and (xx,yy) not in path
                and lines[yy][xx]!="#"]
    else:
        match lines[y][x]:
            case "<": next = [(x-1, y)]
            case ">": next = [(x+1,y)]
            case "^": next = [(x, y-1)]
            case "v": next = [(x, y+1)]
        next = [p for p in next if p not in path]

    new_path = path.union([(x,y)])
    paths = [visit(xx, yy, new_path, slopes) for xx, yy in next]
    
    return 0 if len(paths)==0 else max(paths)

y = 0
x = lines[y].find(".")

adj = {}
for x in range(width):
    for y in range(height):
        if lines[y][x]=="#":
            continue
        next = [(xx,yy) for xx,yy in next_steps(x,y) 
            if 0<=xx and xx<width and 0<=yy and yy<height
            and lines[yy][xx]!="#"]

        adj[(x,y)] = next
            
adj = dict([(a, adj[a]) for a in adj if adj[a]])
vertices = [x for x in adj if len(adj[x])!=2]
edges = []
for v in vertices:
    for e in adj[v]:
        path = set([v])
        # Shorten each edge
        while e not in vertices:
            path.add(e)
            e = [ee for ee in adj[e] if ee not in path][0]
        edges.append((v, e, len(path)))

def visit2(v, path: set = set()):
    if v[1] == height-1:
        return 0
    
    next = [e for e in edges if e[0]==v and e[1] not in path]
    next.sort(key = lambda x: -x[2])
    if len(next)==0:
        # No way forward
        return -1
    new_path = path.union([v])
    temp = [(visit2(e, new_path),w) for _, e, w in next]
    temp = [a+b for a,b in temp if a>=0]
    return max(temp) if len(temp)>0 else -1

print(visit2((1,0)))