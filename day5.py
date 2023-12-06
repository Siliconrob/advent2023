import itertools
from functools import partial
from itertools import groupby
from icecream import ic
from parse import parse
from itertools import count
from aocd import get_data


def parse_seeds_part1(seed_group: list[str]) -> list[int]:
    return [int(seed_number) for seed_number in seed_group.pop().split(":")[1].strip().split(" ")]


def map_translator(start: int, end: int, range: int, input_number: int) -> int:
    limit = range - 1
    if input_number > start + limit or input_number < start:
        return None
    if start > end:
        return input_number - (start - end)
    if end > start:
        return input_number + (end - start)
    return input_number


def map_translator_reverse(start: int, end: int, range: int, input_number: int) -> int:
    limit = range - 1
    if input_number > end + limit or input_number < end:
        return None
    if end > start:
        return input_number - (end - start)
    if start > end:
        return input_number + (start - end)
    return input_number


def parse_mappings(mapping_group: list[str]) -> (str, list[partial]):
    mapping_fns = []
    mapping_name = mapping_group[0]
    for mapping_fn in mapping_group[1:]:
        end, start, range = parse('{:d} {:d} {:d}', mapping_fn)
        new_fn = partial(map_translator, start, end, range)
        mapping_fns.append(new_fn)
    return mapping_name, mapping_fns


def get_mapping_chain_fns(mapping_groupings) -> dict:
    fn_chains = {}
    for input_group in mapping_groupings:
        new_map_name, new_mapping_fns = parse_mappings(input_group)
        fn_chains[new_map_name] = new_mapping_fns
    return fn_chains


def parse_mappings_reversed(mapping_group: list[str]) -> (str, list[partial]):
    mapping_fns = []
    mapping_name = mapping_group[0]
    for mapping_fn in mapping_group[1:]:
        end, start, range = parse('{:d} {:d} {:d}', mapping_fn)
        new_fn = partial(map_translator_reverse, start, end, range)
        mapping_fns.append(new_fn)
    return mapping_name, mapping_fns


def get_reversed_mapping_chain_fns(mapping_groupings) -> dict:
    fn_chains = {}
    for input_group in mapping_groupings:
        new_map_name, new_mapping_fns = parse_mappings_reversed(input_group)
        fn_chains[f'{new_map_name}_reversed'] = new_mapping_fns
    return fn_chains


def part1_solve(mapping_chains: dict, seeds: list[int]) -> int:
    seed_locations = []
    for seed in seeds:
        current = seed
        for map_name, mapping_chain in mapping_chains.items():
            ic(map_name)
            results = ic(
                list(itertools.filterfalse(lambda x: x is None, [map_fn(current) for map_fn in mapping_chain])))
            current = ic(current if len(results) == 0 else results.pop())
        seed_locations.append(current)
    return min(seed_locations)


def range_check(input_test: int):
    for x, y in zip(seeds_part1[::2], seeds_part1[1::2]):
        if x <= input_test < x + y:
            return True
    return False


def part2_solve(reversed_mapping_chains, input_test_number) -> int:
    start = input_test_number
    for map_name, mapping_chain in reversed_mapping_chains.items():
        ic(map_name)
        results = ic(list(itertools.filterfalse(lambda x: x is None, [map_fn(start) for map_fn in mapping_chain])))
        start = ic(start if len(results) == 0 else results.pop())
    return start


if __name__ == '__main__':
    # data = get_data(day=5, year=2023).splitlines()
    data = ['seeds: 79 14 55 13',
            '',
            'seed-to-soil map:',
            '50 98 2',
            '52 50 48',
            '',
            'soil-to-fertilizer map:',
            '0 15 37',
            '37 52 2',
            '39 0 15',
            '',
            'fertilizer-to-water map:',
            '49 53 8',
            '0 11 42',
            '42 0 7',
            '57 7 4',
            '',
            'water-to-light map:',
            '88 18 7',
            '18 25 70',
            '',
            'light-to-temperature map:',
            '45 77 23',
            '81 45 19',
            '68 64 13',
            '',
            'temperature-to-humidity map:',
            '0 69 1',
            '1 0 69',
            '',
            'humidity-to-location map:',
            '60 56 37',
            '56 93 4']

    input_groups = [list(g) for k, g in groupby(data, key=lambda x: x == '') if not k]
    seeds_part1 = ic(parse_seeds_part1(input_groups[0]))
    mapping_chains = get_mapping_chain_fns(input_groups[1:])
    ic(f'Part 1: {part1_solve(mapping_chains, seeds_part1)}')

    new_groups = input_groups[1:]
    new_groups.reverse()

    reversed_mapping_chains = get_reversed_mapping_chain_fns(new_groups)
    for test_number in count():
        possible_seed_result = ic(part2_solve(reversed_mapping_chains, test_number))
        if range_check(possible_seed_result):
            ic(f'Part 2 {test_number}')
            break