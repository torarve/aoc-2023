import re

def read_file() -> list[str]:
    with open("input05.txt") as f:
        lines = [x.strip() for x in f.readlines()]
        return lines


lines = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4""".split("\n")

lines = read_file()

# print(lines)

seeds = [int(x) for x in re.findall(r"\d+", lines[0])]

maps: dict[str, list[tuple[int,int,int]]] = {}
i = 2
while i<len(lines):
    current = lines[i][:-5]
    print(current)
    ranges = []
    i += 1
    while i<len(lines) and lines[i]!='':
        ranges.append(tuple(
            [int(x) for x in lines[i].split(" ")]))
        i += 1
    i += 1
    maps[current] = ranges
    

# Part 1
locations = []
location = seeds[0]
for location in seeds:
    current = "seed"
    while True:
        # print(f"{current} {location} -> ")
        next = [x for x in maps.keys() if x.startswith(current)]
        if len(next) == 0:
            break
        key = next[0]
        ranges = maps[key]
        dest = [(destStart, srcStart, length)
                for (destStart, srcStart, length) in (ranges)
                if location>=srcStart and location<=srcStart+length]
        if len(dest)>0:
            destStart, srcStart, length = dest[0]
            location = destStart + (location-srcStart)
        
        current = key[len(current)+len("-to-"):]
    # print(location)
    locations.append(location)
    
print(min(locations))


def split_range(range: tuple[int,int], dStart, sStart, dLength):
    """Split range according to mapping.
    Returns mapped range and any excess"""
    start, length = range
    if start>=sStart+dLength or start+length<=sStart:
        return None, [range]
    
    # convering
    if sStart<=start and start+length<=sStart+dLength:
        if dStart+(start-sStart) ==0:
            pass
        return (dStart + (start-sStart), length), []
    # beginning
    if sStart<=start and start+length>sStart+dLength:
        offset = start-sStart
        # 0123456789
        # -----
        #    -------
        # ooo
        if dStart+offset ==0:
            pass
        return (dStart + offset, dLength-offset), [(start + (dLength - offset), length - (dLength-offset))]
    # end
    if sStart>start and start+length<=sStart+dLength:
        offset = sStart-start
        if dStart ==0:
            pass
        return (dStart, length-offset), [(start, offset)]
    # inside
    if sStart>start and start+length>sStart+dLength:
        offset = sStart - start
        if dStart+offset ==0:
            pass
        return (dStart+offset, dLength), [(start, offset), (start+offset+dLength, length-dLength-offset)]
    
    print(range, dStart, sStart, dLength)
    raise "Should not happend"

# Part 2
locations = []
location = seeds[0]
for i in range(len(seeds)//2):
    # print(i, seeds[2*i:2*(i+1)])
    pos, length = tuple(seeds[2*i:2*(i+1)])
    working_set: list[tuple[int,int]] = [(pos,length)]
    current = "seed"
    while True:
        next = [x for x in maps.keys() if x.startswith(current)]
        if len(next) == 0:
            break
        key = next[0]
        ranges = maps[key]
        
        temp = []
        # For each range
        for start, length in working_set:
            remaining = [(start, length)]
            # Find each overlapping range
            dest = [(destStart, srcStart, length)
                    for (destStart, srcStart, length) in (ranges)
                    if not (start+length<=srcStart or start>srcStart+length)]
            for dStart, sStart, dLength in dest:
                rr = []
                for r in remaining:
                    a, b = split_range(r, dStart, sStart, dLength)
                    if a is not None:
                        temp.append(a)
                    rr.extend(b)
                remaining = rr        
            temp.extend(remaining)
            
        working_set = temp
        # print(temp)
        current = key[len(current)+len("-to-"):]
    locations.append(min([a for a,b in working_set]))
    print(f"{i+1} of {len(seeds)//2}")
    print(min(locations))
    
print(min(locations))