import itertools
import math
import re
from dataclasses import dataclass
from parse import parse
from aocd import get_data
from icecream import ic
from collections import deque


@dataclass
class Card:
    id: int
    winning_numbers: list[int]
    game_numbers: list[int]
    instances: int = 1

    def matches(self):
        return list(set(self.game_numbers) & set(self.winning_numbers))

    def score(self):
        matches = len(self.matches())
        if matches == 0:
            return 0
        return math.pow(2, matches - 1)


def parse_card(card_input: str) -> Card:
    card_parts = card_input.split("|")
    win_section = card_parts[0].split(":")
    card_id = int(re.findall('\d', win_section[0])[0])
    winning_numbers = [int(valid_number) for valid_number in
                       list(itertools.filterfalse(lambda x: x == '', [number for number in win_section[1].split(" ")]))]
    game_numbers = [int(valid_number) for valid_number in
                    list(itertools.filterfalse(lambda x: x == '', [number for number in card_parts[1].split(" ")]))]
    return ic(Card(card_id, winning_numbers, game_numbers))


if __name__ == '__main__':
    # data = get_data(day=4, year=2023).splitlines()
    data = ['Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53',
            'Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19',
            'Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1',
            'Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83',
            'Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36',
            'Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11']

    game_cards = [parse_card(card_line) for card_line in data]
    part1 = sum([game_card.score() for game_card in game_cards])
    ic(f'Part 1: {part1}')

    for index, card in enumerate(game_cards):
        matches = len(card.matches())
        if matches == 0:
            continue
        while matches > 0:
            if matches + index < len(game_cards):
                cards_to_add = card.instances if card.instances > 1 else 1
                game_cards[index + matches].instances += cards_to_add
            matches -= 1
    ic(game_cards)
    part2 = sum(card.instances for card in game_cards)
    ic(f'Part 2: {part2}')
