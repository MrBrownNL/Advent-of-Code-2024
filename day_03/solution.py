import re
from modules.data_processor import get_puzzle_input


def get_sum_multiplications(memory_string):
    mul_pattern = r'mul\((\d{1,3}),(\d{1,3})\)'

    matches = re.findall(mul_pattern, memory_string)

    total = 0
    for x, y in matches:
        total += int(x) * int(y)

    return total


def get_sum_enabled_multiplications(memory_string):
    mul_pattern = re.compile(r'mul\((\d+),(\d+)\)')
    do_pattern = re.compile(r"do\(\)")
    dont_pattern = re.compile(r"don't\(\)")

    mul_enabled = True
    total_sum = 0

    memory_string = memory_string.replace(' ', '')

    for match in re.finditer(r'(mul\(\d+,\d+\)|do\(\)|don\'t\(\))', memory_string):
        instruction = match.group(0)

        if mul_pattern.match(instruction):
            if mul_enabled:
                a, b = map(int, instruction[4:-1].split(','))
                total_sum += a * b

        elif do_pattern.match(instruction):
            mul_enabled = True

        elif dont_pattern.match(instruction):
            mul_enabled = False

    return total_sum


def solve_part_1(input_string):
    return get_sum_multiplications(input_string)


def solve_part_2(input_string):
    return get_sum_enabled_multiplications(input_string)


if __name__ == '__main__':
    input_memory = get_puzzle_input(day=3)

    result_part_1 = get_sum_multiplications(input_memory)
    print(f"Puzzle result part 1: {result_part_1}")

    result_part_2 = get_sum_enabled_multiplications(input_memory)
    print(f"Puzzle result part 2: {result_part_2}")
