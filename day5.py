import itertools
from functools import partial
from itertools import groupby
from icecream import ic
from parse import parse


def parse_seeds(seed_group: list[str]) -> list[int]:
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
    seeds = parse_seeds(input_groups[0])
    ic(seeds)

    mapping_chains = get_mapping_chain_fns(input_groups[1:])
    ic(f'Part 1: {part1_solve(mapping_chains, seeds)}')
