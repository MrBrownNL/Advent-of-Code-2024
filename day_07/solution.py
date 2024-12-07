from modules.data_processor import get_puzzle_input
from itertools import product


def evaluate_expression(nums, ops):
    result = nums[0]

    for num, op in zip(nums[1:], ops):
        if op == '+':
            result += num
        elif op == '*':
            result *= num
        elif op == '||':
            result = int(str(result) + str(num))

    return result


def solve_equation(test_value, numbers, operators):
    num_operators = len(numbers) - 1

    for ops in product(operators, repeat=num_operators):
        if evaluate_expression(numbers, ops) == test_value:
            return True
    return False


def calculate_calibration_result(input, operators):
    total_calibration_result = 0

    for line in input.splitlines():
        test_value_string, numbers_string = line.split(':')
        test_value = int(test_value_string.strip())
        numbers = list(map(int, numbers_string.strip().split()))

        if solve_equation(test_value, numbers, operators):
            total_calibration_result += test_value

    return total_calibration_result


def solve_part_1(input):
    operators = ['+', '*']

    result = calculate_calibration_result(input, operators)

    return result


def solve_part_2(input):
    operators = ['+', '*', '||']

    result = calculate_calibration_result(input, operators)

    return result


if __name__ == '__main__':
    day = 7
    data = get_puzzle_input(day=day)

    result_part_1 = solve_part_1(data)
    print(f"Puzzle result part 1: {result_part_1}")
    # submit_answer(answer=result_part_1, part=1, day=day)

    result_part_2 = solve_part_2(data)
    print(f"Puzzle result part 2: {result_part_2}")
    # submit_answer(answer=result_part_2, part=2, day=day)
