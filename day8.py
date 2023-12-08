from aocd import get_data
from collections import Counter, defaultdict
from dataclasses import dataclass
from parse import parse
from icecream import ic
import networkx as nx
from itertools import cycle


@dataclass
class PathSegment:
    id: str
    left_node_id: str
    right_node_id: str


def part1_solve(directions: str, start_id: str, end_id: str, paths: dict) -> int:
    target = ic(paths[end_id])
    current_node = ic(paths[start_id])

    total_steps = 0
    for next_direction in cycle(directions):
        if current_node.id == target.id:
            break
        if next_direction == 'L':
            current_node = paths[current_node.left_node_id]
            total_steps += 1
            continue
        current_node = paths[current_node.right_node_id]
        total_steps += 1
    return total_steps


def part2_solve(directions: str, ends_with_start_node: str, ends_with_target_node: str, paths: dict) -> int:
    ghost_paths = {}
    for k, v in paths.items():
        if k.endswith(ends_with_start_node):
            ghost_paths[k] = paths[k]

    total_steps = 0
    for next_direction in cycle(directions):
        total_steps += 1
        completed_paths = sum([1 if cv.id.endswith(ends_with_target_node) else 0 for ck, cv in ghost_paths.items()])
        if completed_paths == len(ghost_paths):
            break
        if next_direction == 'L':
            for ck, cv in ghost_paths.items():
                ghost_paths[ck] = paths[cv.left_node_id]
            continue
        for ck, cv in ghost_paths.items():
            ghost_paths[ck] = paths[cv.right_node_id]
    return total_steps - 1


def get_inputs(input_lines: []) -> (str, {}):
    directions = ic(input_lines[0])
    path_segments = {}
    for path_segment in input_lines[2:]:
        id, left_node, right_node = parse('{} = ({}, {})', path_segment)
        path_segments[id] = PathSegment(id, left_node, right_node)
    return directions, path_segments


if __name__ == '__main__':
    data = get_data(day=8, year=2023).splitlines()
    # data = ['RL',
    #         '',
    #         'AAA = (BBB, CCC)',
    #         'BBB = (DDD, EEE)',
    #         'CCC = (ZZZ, GGG)',
    #         'DDD = (DDD, DDD)',
    #         'EEE = (EEE, EEE)',
    #         'GGG = (GGG, GGG)',
    #         'ZZZ = (ZZZ, ZZZ)']
    # data = ['LLR',
    #         '',
    #         'AAA = (BBB, BBB)',
    #         'BBB = (AAA, ZZZ)',
    #         'ZZZ = (ZZZ, ZZZ)']
    # data = ['LR',
    #         '',
    #         '11A = (11B, XXX)',
    #         '11B = (XXX, 11Z)',
    #         '11Z = (11B, XXX)',
    #         '22A = (22B, XXX)',
    #         '22B = (22C, 22C)',
    #         '22C = (22Z, 22Z)',
    #         '22Z = (22B, 22B)',
    #         'XXX = (XXX, XXX)']

    # directions, part1_segments = ic(get_inputs(data))
    # ic(f'Part 1: {part1_solve(directions, 'AAA', 'ZZZ', part1_segments)}')
    directions, part2_segments = ic(get_inputs(data))
    ic(f'Part 2: {part2_solve(directions, 'A', 'Z', part2_segments)}')
