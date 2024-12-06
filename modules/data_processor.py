import os
from pathlib import Path

from dotenv import load_dotenv
from aocd import get_data, submit

load_dotenv()

project_root = Path(__file__).parent.parent

def get_puzzle_input(day):
    filename = f"{project_root}/day_{day:02}/puzzle_input.txt"

    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = file.read()

        return data

    """ 
    I'm using the get_data function here instead of the data function to improve readability 
        and the ability to optimize code for past days
    """
    data = get_data(day=day, year=os.getenv('YEAR'))

    with open(filename, 'w') as file:
        file.write(data)

    return data


def submit_answer(answer: int, day: int, part: int):
    part = {1: "a", 2: "b"}.get(part)
    submit(answer=answer, part=part, day=day, year=os.getenv('YEAR'))
