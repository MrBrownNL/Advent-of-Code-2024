from importlib import import_module
from modules.data_processor import get_puzzle_input
from datetime import datetime


def get_day_input():
    current_day = datetime.now().day

    if current_day > 25:
        current_day = 25

    user_input = input(f"Which day? [{current_day}]: ")
    return int(user_input) if user_input and 1 <= int(user_input) <= 25 else current_day


def get_part_input():
    part = 1

    user_input = input(f"Which part? [{part}]: ")
    return int(user_input) if user_input and 1 <= int(user_input) <= 2 else part


if __name__ == '__main__':
    print("Welcome to the Advent of Code 2024 puzzle solver!")
    day = get_day_input()
    part = get_part_input()

    print(f"Solving puzzle for day {day} part {part}...")

    puzzle_input = get_puzzle_input(day)

    module = import_module(f"day_{day:02}.solution")
    solver = getattr(module, f"solve_part_{part}")
    result = solver(puzzle_input)

    print(f"The answer is: {result}")

