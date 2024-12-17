from modules.data_processor import get_puzzle_input
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Set, Tuple
import re
from collections import defaultdict


@dataclass
class Robot:
    pos_x: int
    pos_y: int
    vel_x: int
    vel_y: int


def parse_input(input_text: str) -> List[Robot]:
    robots = []
    pattern = r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)'

    for line in input_text.strip().split('\n'):
        match = re.match(pattern, line)
        if match:
            px, py, vx, vy = map(int, match.groups())
            robots.append(Robot(px, py, vx, vy))

    return robots


def simulate_robots(robots: List[Robot], width: int, height: int, seconds: int) -> defaultdict:
    # Use modular arithmetic to directly calculate final positions
    positions = defaultdict(int)

    for robot in robots:
        # Calculate final position using modulo to handle wrapping
        final_x = (robot.pos_x + robot.vel_x * seconds) % width
        final_y = (robot.pos_y + robot.vel_y * seconds) % height
        positions[(final_x, final_y)] += 1

    return positions


def calculate_safety_factor(positions: defaultdict, width: int, height: int) -> int:
    # Initialize counters for each quadrant
    quadrants = [0] * 4
    mid_x = width // 2
    mid_y = height // 2

    for (x, y), count in positions.items():
        # Skip robots on the middle lines
        if x == mid_x or y == mid_y:
            continue

        # Determine quadrant (0: top-left, 1: top-right, 2: bottom-left, 3: bottom-right)
        quadrant = (2 if y > mid_y else 0) + (1 if x > mid_x else 0)
        quadrants[quadrant] += count

    # Multiple all quadrant counts
    safety_factor = 1
    for count in quadrants:
        safety_factor *= count

    return safety_factor


def get_positions_at_time(robots: List[Robot], time: int, width: int, height: int) -> Set[Tuple[int, int]]:
    positions = set()
    for robot in robots:
        x = (robot.pos_x + robot.vel_x * time) % width
        y = (robot.pos_y + robot.vel_y * time) % height
        positions.add((x, y))
    return positions


def plot_coordinates(coordinates):
    # Separate x and y coordinates
    x_coords = [x for x, y in coordinates]
    y_coords = [y for x, y in coordinates]

    # Create the plot
    plt.figure(figsize=(10, 10))
    plt.scatter(x_coords, y_coords, c='red', marker='o')

    # Add labels and title
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Coordinate Map')

    # Add grid
    plt.grid(True)

    # Show the plot
    plt.show()


def visualize_positions(positions: Set[Tuple[int, int]]) -> str:
    plot_coordinates(positions)

def visualize_grid(char_grid):
    rows, cols = len(char_grid), len(char_grid[0])

    # Create the plot
    fig, ax = plt.subplots(figsize=(6, 6))

    # Plot each character as text
    for i in range(rows):
        for j in range(cols):
            ax.text(j, i, char_grid[i][j], ha='center', va='center', fontsize=14, color='black')

    # Adjust axes limits and gridlines
    ax.set_xticks(range(cols))
    ax.set_yticks(range(rows))
    ax.set_xlim(-0.5, cols - 0.5)
    ax.set_ylim(-0.5, rows - 0.5)
    ax.invert_yaxis()  # Flip y-axis to match the usual grid orientation
    ax.grid(visible=True, color='gray', linestyle='--')

    # Remove ticks for a cleaner look
    ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

    # Add a title
    plt.title("Character Grid")

    # Show the plot
    plt.show()


def solve_puzzle(input_text: str, width: int = 101, height: int = 103, seconds: int = 100) -> int:
    # Parse input
    robots = parse_input(input_text)

    # Simulate robot movements
    final_positions = simulate_robots(robots, width, height, seconds)

    # Calculate safety factor
    return calculate_safety_factor(final_positions, width, height)


def get_grid(positions: defaultdict):
    new_grid = [['.'] * 105 for _ in range(105)]

    #plot positions
    for position in positions:
        new_grid[position[1]][position[0]] = "*"

    return new_grid

def solve_puzzle_2(input_text: str, width: int = 101, height: int = 103) -> int:
    # Parse input
    robots = parse_input(input_text)

    seconds = 1

    while True:
        # Simulate robot movements
        new_positions = simulate_robots(robots, width, height, seconds)
        # plot positions on a grid
        grid = get_grid(new_positions)

        lines = [''.join(row) for row in grid]
        for line in lines:
            if re.search(r'\*{10}', line):
                visualize_grid(grid)
                return seconds

        seconds += 1


def solve_part_1(data) -> int:
    return solve_puzzle(data.strip())


def solve_part_2(data) -> int:
    return solve_puzzle_2(data.strip())



if __name__ == '__main__':
    day = 14
    data = get_puzzle_input(day=day)

    # result_part_1 = solve_part_1(data)
    # print(f"Puzzle result part 1: {result_part_1}")

    result_part_2 = solve_part_2(data)
    print(f"Puzzle result part 2: {result_part_2}")
