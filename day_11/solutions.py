from modules.data_processor import get_puzzle_input


def get_stones(puzzle_input):
    return list(map(int, puzzle_input.strip().split()))


def solve_part_1(input):
    stones = get_stones(input)

    def process_stone(stone):
        if stone == 0:
            new_stones.append(1)
        elif len(str(stone)) % 2 == 0:
            half_stone_length = int(len(str(stone)) / 2)
            left = int(str(stone)[:half_stone_length])
            right = int(str(stone)[half_stone_length:])
            new_stones.extend([left, right])
        else:
            new_stones.append(stone * 2024)

    for i in range(25):
        new_stones = []
        for stone in stones:
            process_stone(stone)

        stones = new_stones

    return len(stones)


def solve_part_2(input):
    pass


if __name__ == '__main__':
    day = 11
    data = get_puzzle_input(day=day)

    result_part_1 = solve_part_1(data)
    print(f"Puzzle result part 1: {result_part_1}")

    result_part_2 = solve_part_2(data)
    print(f"Puzzle result part 2: {result_part_2}")
