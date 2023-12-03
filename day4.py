import itertools
import math
from dataclasses import dataclass
from parse import parse
from aocd import get_data
from icecream import ic
from collections import deque


def get_symbol_part(check_row_index: int, check_col_index: int, row_data: str, all_rows: []) -> int:
    if -1 < check_row_index < len(data) and -1 < check_col_index < len(row_data):
        target_row = all_rows[check_row_index]
        target_char = target_row[check_col_index]
        if target_char.isnumeric():
            return get_number(target_row, check_col_index)
    return None


def get_number(row_text: str, start_index: int) -> int:
    left_side = [*row_text[:start_index]]
    right_side = deque([*row_text[start_index:]])

    current_digits = []
    while left_side:
        current_element = left_side.pop()
        if current_element.isnumeric():
            current_digits.append(current_element)
        else:
            break

    current_digits.reverse()
    while right_side:
        current_element = right_side.popleft()
        if current_element.isnumeric():
            current_digits.append(current_element)
        else:
            break

    number_text = ''.join(digit for digit in current_digits)
    return ic(int(number_text))


def get_uniques(input_numbers: dict) -> list[int]:
    uniques = []
    for the_number in input_numbers.values():
        if the_number is not None:
            uniques.append(the_number)
    return uniques


if __name__ == '__main__':
    # data = get_data(day=4, year=2023).splitlines()
    data = ['467..114..',
            '...*......',
            '..35..633.',
            '......#...',
            '617*......',
            '.....+.58.',
            '..592.....',
            '......755.',
            '...$.*....',
            '.664.598..']

    part_numbers = []
    gear_ratios = []

    for row_index, row_data in enumerate(data):
        symbol_parts = []
        for col_index, col_value in enumerate(row_data):
            if col_value.isnumeric() or col_value == '.':
                continue

            top_numbers = {'left': get_symbol_part(row_index - 1, col_index - 1, row_data, data),
                           'above': get_symbol_part(row_index - 1, col_index, row_data, data),
                           'right': get_symbol_part(row_index - 1, col_index + 1, row_data, data)}

            if top_numbers['left'] == top_numbers['above']:
                top_numbers['left'] = None
            if top_numbers['right'] == top_numbers['above']:
                top_numbers['right'] = None

            number_positions = {'left': get_symbol_part(row_index, col_index - 1, row_data, data),
                                'right': get_symbol_part(row_index, col_index + 1, row_data, data)}

            bottom_numbers = {'left': get_symbol_part(row_index + 1, col_index - 1, row_data, data),
                              'below': get_symbol_part(row_index + 1, col_index, row_data, data),
                              'right': get_symbol_part(row_index + 1, col_index + 1, row_data, data)}

            if bottom_numbers['left'] == bottom_numbers['below']:
                bottom_numbers['left'] = None
            if bottom_numbers['right'] == bottom_numbers['below']:
                bottom_numbers['right'] = None

            total_uniques = list(itertools.chain(get_uniques(top_numbers), get_uniques(number_positions), get_uniques(bottom_numbers)))
            symbol_parts.extend(total_uniques)

            if col_value == '*' and len(total_uniques) > 1:
                gear_ratios.append(ic(math.prod(total_uniques)))

        if len(symbol_parts) > 0:
            part_numbers.extend(symbol_parts)

    part1 = sum(part_numbers)
    ic(f'Part 1: {part1}')
    part2 = sum(gear_ratios)
    ic(f'Part 2: {part2}')
