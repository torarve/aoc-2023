from functools import reduce
from operator import mul


def read_file() -> list[str]:
    with open("input02.txt") as f:
        lines = [x.strip() for x in f.readlines()]
        return lines
    
def parse_line(line: str) -> list[dict[str,int]]:
    def parse(x: str) -> tuple[str, int]:
        a, b = tuple(x.split(" "))
        return (b, int(a))
    
    def parse_set(set: str):
        return dict([parse(x) for x in set.split(", ")])
    
    split = line.find(":")
    game = line[5:split]
    sets = [parse_set(x) for x in line[split+2:].split("; ") ]
    return (game, sets)
    
def check_part_1(sets: list[dict[str,int]]) -> bool:
    for set in sets:
        if set.get("red",0)>12 or set.get("green", 0)>13 or set.get("blue", 0)>14:
            return False
    return True 

def minimum_set(sets: list[dict[str,int]]) -> dict[str, int]:
    result = {}
    for set in sets:
        for color, amount in set.items():
            if result.get(color, 0)<amount:
                result[color] = amount
    return result

def power(sets: list[dict[str,int]]) -> int:
    return reduce(mul, minimum_set(sets).values())


lines = [
    "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
    "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
    "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
    "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
    "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"
]

lines = read_file()
games = [parse_line(line) for line in lines]

allowed_games = [int(game) for game, sets in games if check_part_1(sets)]
print(sum(allowed_games))

powers = [power(sets) for _, sets in games]
print(sum(powers))
