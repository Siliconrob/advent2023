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


def part1_solve(start_id: str, end_id: str, paths: dict) -> int:
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

    directions = ic(data[0])

    # G = nx.DiGraph()
    path_segments = {}
    for path_segment in data[2:]:
        id, left_node, right_node = parse('{} = ({}, {})', path_segment)
        path_segments[id] = PathSegment(id, left_node, right_node)
        # segments.append(PathSegment(current_node, left_node, right_node, path_segment))
        # G.add_node(current_node)
        # G.add_edge(current_node, left_node, weight='L')
        # G.add_edge(current_node, right_node, weight='R')

    keys = list(path_segments.keys())

    ic(f'Part 1: {part1_solve('AAA', 'ZZZ', path_segments)}')
