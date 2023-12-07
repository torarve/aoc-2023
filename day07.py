from functools import cmp_to_key
from itertools import groupby


def read_file() -> list[str]:
    with open("input07.txt") as f:
        lines = [x.strip() for x in f.readlines()]
        return lines
    

lines = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""".split("\n")

lines = read_file()

def parse_line(line: str) -> (list[str], int):
    return line[:5], int(line[6:])

FIVE_OF_A_KIND = 6
FOUR_OF_A_KIND = 5
FULL_HOUSE = 4
THREE_OF_A_KIND = 3
TWO_PAIR = 2
ONE_PAIR = 1
HIGH_CARD = 0

def value(card: str) -> int:
    return "23456789TJQKA".index(card)

def value_of_hand(hand: str) -> int:
    hand_values = [value(card) for card in hand]
    grouped = [(k, len(list(g))) for k, g in groupby(sorted(hand_values))]
    counts = sorted([b for a,b in grouped])
    values = tuple(hand_values)
    if max(counts) == 1:
        return HIGH_CARD, values
    elif counts[-1] == 2 and counts[-2] == 1:
        return ONE_PAIR, values
    elif counts[-1] == 2 and counts[-2] == 2:
        return TWO_PAIR, values
    elif counts[-1] == 3 and counts[-2] == 1:
        return THREE_OF_A_KIND, values
    elif counts[-1] == 3 and counts[-2] == 2:
        return FULL_HOUSE, values
    elif counts[-1] == 4:
        return FOUR_OF_A_KIND, values
    elif counts[-1] == 5:
        return FIVE_OF_A_KIND, values
    
    raise "Should never happen"

parsed_hands = [parse_line(line) for line in lines]    
hands = [(value_of_hand(hand), bid) for hand, bid in parsed_hands]

def compare_hands(hand1, hand2) -> int:
    tmp1, _ = hand1
    tmp2, _ = hand2
    if tmp1[0]==tmp2[0]:
        for i in range(5):
            if tmp1[1][i] != tmp2[1][i]:
                return tmp1[1][i] - tmp2[1][i]
        return 0
    else:
        return tmp1[0]-tmp2[0]

sorted_hands = sorted(hands, key=cmp_to_key(compare_hands))
winnings = [(i+1)*bid for i, (hand, bid) in enumerate(sorted_hands)]
print(sum(winnings))

def value2(card: str) -> int:
    return "J23456789TQKA".index(card)

def value_of_hand2(hand: str) -> int:
    hand_values = [value2(card) for card in hand]
    if "J" in hand:
        possible = [value_of_hand2(hand.replace("J", j))
                                   for j in "23456789TQKA"]
        best = max(possible, key=lambda x: x[0])
        return best[0], hand_values

    grouped = [(k, len(list(g))) for k, g in groupby(sorted(hand_values))]
    counts = sorted([b for a,b in grouped])
    values = tuple(hand_values)
    if max(counts) == 1:
        return HIGH_CARD, values
    elif counts[-1] == 2 and counts[-2] == 1:
        return ONE_PAIR, values
    elif counts[-1] == 2 and counts[-2] == 2:
        return TWO_PAIR, values
    elif counts[-1] == 3 and counts[-2] == 1:
        return THREE_OF_A_KIND, values
    elif counts[-1] == 3 and counts[-2] == 2:
        return FULL_HOUSE, values
    elif counts[-1] == 4:
        return FOUR_OF_A_KIND, values
    elif counts[-1] == 5:
        return FIVE_OF_A_KIND, values
    
    raise "Should never happen"

def compare_hands2(hand1, hand2) -> int:
    tmp1, _ = hand1
    tmp2, _ = hand2
    if tmp1[0]==tmp2[0]:
        for i in range(5):
            if tmp1[1][i] != tmp2[1][i]:
                return tmp1[1][i] - tmp2[1][i]
        return 0
    else:
        return tmp1[0]-tmp2[0]

hands2 = [(value_of_hand2(hand), bid) for hand, bid in parsed_hands]
sorted_hands2 = sorted(hands2, key=cmp_to_key(compare_hands2))
winnings2 = [(i+1)*bid for i, (hand, bid) in enumerate(sorted_hands2)]
print(sum(winnings2))
