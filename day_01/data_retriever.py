def get_puzzle_input():
    first_column = []
    second_column = []

    with open('puzzle_input.txt', 'r') as file:
        for line in file:
            nums = line.strip().split()

            first_column.append(int(nums[0]))
            second_column.append(int(nums[1]))

    return first_column, second_column
