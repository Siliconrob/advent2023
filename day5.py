import itertools
import math
import re
from dataclasses import dataclass
from parse import parse
from aocd import get_data
from icecream import ic
from collections import deque
from itertools import groupby
from functools import partial


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


def parse_mappings(mapping_group: list[str]) -> list[partial]:
    mapping_fns = []
    for mapping_fn in mapping_group[1:]:
        end, start, range = parse('{:d} {:d} {:d}', mapping_fn)
        new_fn = partial(map_translator, start, end, range)
        mapping_fns.append(new_fn)
    return mapping_fns


if __name__ == '__main__':
    data = get_data(day=5, year=2023).splitlines()
    # data = ['seeds: 79 14 55 13',
    #         '',
    #         'seed-to-soil map:',
    #         '50 98 2',
    #         '52 50 48',
    #         '',
    #         'soil-to-fertilizer map:',
    #         '0 15 37',
    #         '37 52 2',
    #         '39 0 15',
    #         '',
    #         'fertilizer-to-water map:',
    #         '49 53 8',
    #         '0 11 42',
    #         '42 0 7',
    #         '57 7 4',
    #         '',
    #         'water-to-light map:',
    #         '88 18 7',
    #         '18 25 70',
    #         '',
    #         'light-to-temperature map:',
    #         '45 77 23',
    #         '81 45 19',
    #         '68 64 13',
    #         '',
    #         'temperature-to-humidity map:',
    #         '0 69 1',
    #         '1 0 69',
    #         '',
    #         'humidity-to-location map:',
    #         '60 56 37',
    #         '56 93 4']

    input_groups = [list(g) for k, g in groupby(data, key=lambda x: x == '') if not k]
    seeds = parse_seeds(input_groups[0])
    ic(seeds)

    mapping_chains = []
    seed_to_soil_map_fns = parse_mappings(input_groups[1])
    mapping_chains.append(seed_to_soil_map_fns)

    soil_to_fertilizer_map_fns = parse_mappings(input_groups[2])
    mapping_chains.append(soil_to_fertilizer_map_fns)

    fertilizer_to_water_map_fns = parse_mappings(input_groups[3])
    mapping_chains.append(fertilizer_to_water_map_fns)

    water_to_light_map_fns = parse_mappings(input_groups[4])
    mapping_chains.append(water_to_light_map_fns)

    light_to_temperature_map_fns = parse_mappings(input_groups[5])
    mapping_chains.append(light_to_temperature_map_fns)

    temperature_to_humidity_map_fns = parse_mappings(input_groups[6])
    mapping_chains.append(temperature_to_humidity_map_fns)

    humidity_to_location_map_fns = parse_mappings(input_groups[7])
    mapping_chains.append(humidity_to_location_map_fns)

    ic(mapping_chains)

    seed_locations = []

    for seed in seeds:
        current = seed
        for mapping_chain in mapping_chains:
            results = ic(
                list(itertools.filterfalse(lambda x: x is None, [map_fn(current) for map_fn in mapping_chain])))
            current = ic(current if len(results) == 0 else results.pop())
        seed_locations.append(current)
    ic(f'Part 1: {min(seed_locations)}')
