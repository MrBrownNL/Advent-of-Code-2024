from modules.data_processor import get_puzzle_input

"""
Get puzzle input:
    Get comma seperated towel patterns
    one blank line
    Get towel designs (one on each line)

Solve part 1:
    How many designs can be made using the patterns?
        check designs by looping over all possible patterns and check the remaining part of the design until remaining part is null (valid) or not null (not valid)

Solve part 2:
    Sum all possible ways to make the designs
    Start with all valid designs from part 1 to speed up the process
    Modify check function from part 1 to return the total possible arrangements
"""


def parse_input(input_data):
    lines = input_data.strip().split('\n')
    patterns = lines[0].strip().split(', ')

    designs = []
    for i, line in enumerate(lines):
        if i < 2:
            continue

        designs.append(line)

    return patterns, designs



def is_valid_design(design, patterns, memo=None):
    if memo is None:
        memo = {}

    if not design:
        # no remaining parts to check
        return True

    if design in memo:
        return memo[design]

    # Check the start of the (remaining) design
    for pattern in patterns:
        if design.startswith(pattern):
            remaining = design[len(pattern):]
            if is_valid_design(remaining, patterns, memo):
                memo[design] = True
                return True

    memo[design] = False

    return False


def count_arrangements(design, patterns, memo=None):
    if memo is None:
        memo = {}

    if not design:
        return 1

    if design in memo:
        return memo[design]

    total = 0

    for pattern in patterns:
        if design.startswith(pattern):
            remaining = design[len(pattern):]
            total += count_arrangements(remaining, patterns, memo)

    memo[design] = total

    return total


def solve_part_1(input_data):
    valid_designs = []

    patterns, designs = parse_input(input_data)
    valid_design_count = 0

    for design in designs:
        if is_valid_design(design, patterns):
            valid_designs.append(design)
            valid_design_count += 1

    return valid_design_count, valid_designs


def solve_part_2(input_data, valid_designs):
    patterns, designs = parse_input(input_data)
    total_arrangements = 0

    for valid_design in valid_designs:
        total_arrangements += count_arrangements(valid_design, patterns)

    return total_arrangements


if __name__ == '__main__':
    day = 19
    input_data = get_puzzle_input(day=day)

    result_part_1, valid_designs = solve_part_1(input_data)
    print(f"Puzzle result part 1: {result_part_1}")

    result_part_2 = solve_part_2(input_data, valid_designs)
    print(f"Puzzle result part 2: {result_part_2}")
