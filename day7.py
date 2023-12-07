from aocd import get_data
from collections import Counter, defaultdict
from dataclasses import dataclass
from parse import parse
from icecream import ic


rank_part1 = str.maketrans("AKQJT98765432", "abcdefghijklm")
rank_part2 = str.maketrans("AKQT98765432J", "abcdefghijklm")

@dataclass
class PlayerAction:
    hand: str
    bid_amount: int


@dataclass
class RankedGroups:
    five_of_a_kind = []
    four_of_a_kind = []
    full_house = []
    three_of_a_kind = []
    two_pair = []
    one_pair = []
    high_card = []

    def sort_group_ranking(self, ranker):
        return [*sorted(self.five_of_a_kind, key=lambda x: x.hand.translate(ranker)),
                *sorted(self.four_of_a_kind, key=lambda x: x.hand.translate(ranker)),
                *sorted(self.full_house, key=lambda x: x.hand.translate(ranker)),
                *sorted(self.three_of_a_kind, key=lambda x: x.hand.translate(ranker)),
                *sorted(self.two_pair, key=lambda x: x.hand.translate(ranker)),
                *sorted(self.one_pair, key=lambda x: x.hand.translate(ranker)),
                *sorted(self.high_card, key=lambda x: x.hand.translate(ranker))]


def parse_player_action(player_round: str) -> PlayerAction:
    hand, bid = parse('{} {:d}', player_round)
    return PlayerAction(hand, bid)


def replace_jokers(input_hand: str) -> str:
    if input_hand.find('J') == -1:
        return input_hand

    new_hand = input_hand.replace('J', '')
    if len(new_hand) == 0:
        return input_hand

    current_counts = Counter(input_hand.replace('J', ''))
    current_max_letter, current_max_count = current_counts.most_common(1)[0]
    for current_letter, current_letter_count in current_counts.items():
        if current_letter_count < current_max_count:
            continue
        if current_letter_count > current_max_count:
            current_max_letter = current_letter
            current_max_count = current_letter_count
            continue
        if "AKQT98765432".index(current_letter) < "AKQT98765432".index(current_max_letter):
            current_max_letter = current_letter
            current_max_count = current_letter_count
    return ic(input_hand.replace("J", current_max_letter))


def rank_hands(hands: list[PlayerAction], part1: bool) -> list[PlayerAction]:
    ranked_groups = RankedGroups()
    for hand in hands:
        uniques = Counter(hand.hand if part1 else replace_jokers(hand.hand))
        if len(uniques.keys()) == 1:
            ranked_groups.five_of_a_kind.append(hand)
            continue
        if len(uniques.keys()) == 2:
            top_cards, bottom_cards = uniques.most_common(2)
            if top_cards[1] == 4:
                ranked_groups.four_of_a_kind.append(hand)
            elif top_cards[1] == 3 and bottom_cards[1] == 2:
                ranked_groups.full_house.append(hand)
            continue
        if len(uniques.keys()) == 3 and uniques.most_common(1)[0][1] == 3:
            ranked_groups.three_of_a_kind.append(hand)
            continue
        remaining_ranks = uniques.most_common(5)
        if len(remaining_ranks) == 5:
            ranked_groups.high_card.append(hand)
            continue
        first_rank = remaining_ranks[0]
        second_rank = remaining_ranks[1]
        if first_rank[1] == second_rank[1]:
            ranked_groups.two_pair.append(hand)
            continue
        ranked_groups.one_pair.append(hand)

    ordered_hands = ic(ranked_groups.sort_group_ranking(rank_part1 if part1 else rank_part2))
    return ordered_hands


def solve_game(input_data: list[str], part1: bool=True) -> int:
    current_game = [parse_player_action(input_line) for input_line in input_data]
    ranked_game = rank_hands(current_game, part1)
    product = 0
    for i, player_hand in enumerate(reversed(ranked_game)):
        product += ic((i + 1) * player_hand.bid_amount)
    return product


if __name__ == '__main__':
    # data = get_data(day=7, year=2023).splitlines()
    data = ['32T3K 765',
            'T55J5 684',
            'KK677 28',
            'KTJJT 220',
            'QQQJA 483']
    ic(f'Part 1: {solve_game(data)}')
    ic(f'Part 2: {solve_game(data, False)}')
