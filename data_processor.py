import os
from numbers import Number
from typing import Literal

from dotenv import load_dotenv
from aocd import get_data, submit

load_dotenv()


def get_puzzle_input(day):
    filename = 'puzzle_input.txt'

    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = file.read()

        return data

    data = get_data(day=day, year=os.getenv('YEAR'))

    with open(filename, 'w') as file:
        file.write(data)

    return data


def submit_answer(answer: Number, day: int, part: Literal[1,2]):
    part = {1: "a", 2: "b"}.get(part)
    submit(answer=answer, part=part, day=day, year=os.getenv('YEAR'))
