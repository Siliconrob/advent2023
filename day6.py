import itertools
import math
from dataclasses import dataclass
from functools import partial
from itertools import groupby
from icecream import ic
from parse import parse
from itertools import count
from aocd import get_data


def run_race(end: int, record: int, start_time: int) -> int:
    if start_time >= end:
        return 0
    travel_distance = (end - start_time) * start_time
    if travel_distance <= record:
        return 0
    return travel_distance


@dataclass
class WinningTime:
    hold_time: int
    distance: int


@dataclass
class RaceRecord:
    time: int
    distance: int


def parse_numbers_from_line(input_line: str) -> list[int]:
    return [int(valid_number) for valid_number in list(
        itertools.filterfalse(lambda x: x == '', [number for number in input_line.split(":")[1].strip().split(" ")]))]


def parse_race_records(race_times: str, race_distances: str) -> list[RaceRecord]:
    times = parse_numbers_from_line(race_times)
    distances = parse_numbers_from_line(race_distances)
    return [RaceRecord(race_time, race_distance) for race_time, race_distance in zip(times, distances)]


if __name__ == '__main__':
    #data = get_data(day=6, year=2023).splitlines()
    data = ['Time:      7  15   30',
            'Distance:  9  40  200']

    parsed_race_records = ic(parse_race_records(data[0], data[1]))
    race_strategies = {}
    for race_record in parsed_race_records:
        current_race_winners = []
        for hold_time in range(0, race_record.time):
            new_record = run_race(race_record.time, race_record.distance, hold_time)
            if new_record > 0:
                current_race_winners.append(WinningTime(hold_time, new_record))
        race_strategies[race_record.time] = current_race_winners
    winning_strategies = []
    for race, winners in race_strategies.items():
        winning_strategies.append(len(winners))
    ic(f'Part 1: {math.prod(winning_strategies)}')
