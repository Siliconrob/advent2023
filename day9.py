from collections import deque
import numpy as np
from aocd import get_data
from icecream import ic


#  This doesn't work right, but problem requires recursion
def calc_value(current_stack: deque, current_number: int, current_diff: int) -> int:
    if len(current_stack) == 0:
        return current_diff
    next_left = current_stack.pop()
    current_diff = current_number - next_left
    if current_diff != 0:
        return ic(current_diff - calc_value(current_stack, next_left, current_diff))
    return current_diff


if __name__ == '__main__':
    data = get_data(day=9, year=2023).splitlines()
    # data = ['0 3 6 9 12 15',
    #         '1 3 6 10 15 21',
    #         '10 13 16 21 30 45']

    current_sums = []
    for input_line in data:
        current_line = [int(number.strip()) for number in input_line.split(" ")]
        results = []
        # https://numpy.org/doc/stable/reference/generated/numpy.diff.html
        for current_number in range(len(current_line)):
            new_row = np.diff(current_line, n=current_number)
            results.append(new_row[-1])
        current_sums.append(ic(sum(results)))
    ic(f'Part 1: {sum(current_sums)}')
    #     current_number = ic(current_line.pop())
    #     #current_sums.append(ic(current_number + calc_value(current_line, current_number, 0)))
    #     current_sums.append(ic(calc_value(current_line, current_number, 0)))
    # ic(current_sums)
