from collections import deque
import numpy as np
from aocd import get_data
from icecream import ic

if __name__ == '__main__':
    #data = get_data(day=9, year=2023).splitlines()
    data = ['0 3 6 9 12 15',
            '1 3 6 10 15 21',
            '10 13 16 21 30 45']

    part1_sums = []
    for input_line in data:
        current_line_part1 = [int(number.strip()) for number in input_line.split(" ")]
        part1_results = []
        # https://numpy.org/doc/stable/reference/generated/numpy.diff.html
        # Tried to do vstack as well but no success https://numpy.org/doc/stable/reference/generated/numpy.vstack.html#numpy-vstack
        for current_number in range(len(current_line_part1)):
            new_row_part1 = np.diff(current_line_part1, n=current_number)
            part1_results.append(new_row_part1[-1])
        part1_sums.append(ic(sum(part1_results)))
    ic(f'Part 1: {sum(part1_sums)}')

    part2_data = ['10 13 16 21 30 45']
    part2_data = data
    part2_sums = []
    for input_line in part2_data:
        current_line_part2 = [int(number.strip()) for number in input_line.split(" ")]
        part2_results = []
        # reverse the inputs to do the prediction for numpy.diff
        reversed_line = current_line_part2[::-1]
        # https://numpy.org/doc/stable/reference/generated/numpy.diff.html
        for current_number in range(len(reversed_line)):
            new_row_part2 = np.diff(reversed_line, n=current_number)
            part2_results.append(new_row_part2[-1])
        part2_sums.append(ic(sum(part2_results)))
    ic(f'Part 2: {sum(part2_sums)}')
