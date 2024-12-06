import time
from modules.data_processor import get_puzzle_input


def parse_input(input):
    return [list(line.strip()) for line in input.strip().split('\n')]


def find_xmas_occurrences(grid):
    """
    Find all occurrences of 'XMAS' in a 2D grid.

    The word can be:
    - Horizontal (left to right or right to left)
    - Vertical (top to bottom or bottom to top)
    - Diagonal (in 4 possible directions)

    Args:
        grid (List[str]): 2D grid of characters

    Returns:
        int: Total number of 'XMAS' occurrences
    """
    rows = len(grid)
    cols = len(grid[0])
    target = "XMAS"

    directions = [
        (0, 1),    # right
        (0, -1),   # left
        (1, 0),    # down
        (-1, 0),   # up
        (1, 1),    # down-right
        (1, -1),   # down-left
        (-1, 1),   # up-right
        (-1, -1)   # up-left
    ]

    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols

    def check_word(x, y, dx, dy):
        """
        Check if 'XMAS' can be found starting from (x,y) in direction (dx,dy).

        Args:
            x (int): Starting row
            y (int): Starting column
            dx (int): Row direction
            dy (int): Column direction

        Returns:
            bool: True if 'XMAS' is found, False otherwise
        """
        for i, letter in enumerate(target):
            nx, ny = x + i*dx, y + i*dy
            if not is_valid(nx, ny) or grid[nx][ny] != letter:
                return False
        return True

    xmas_count = 0
    for x in range(rows):
        for y in range(cols):
            for dx, dy in directions:
                if check_word(x, y, dx, dy):
                    xmas_count += 1

    return xmas_count


def count_xmas_patterns(grid):
    """
    Count the number of diagonal MAS/SAM patterns in 3x3 subgrids of the grid.
    """
    rows, cols = len(grid), len(grid[0])
    xmas_count = 0

    for r in range(rows - 2):
        for c in range(cols - 2):
            if grid[r + 1][c + 1].upper() != "A":
                continue

            main_diagonal = [grid[r][c], grid[r + 1][c + 1], grid[r + 2][c + 2]]
            anti_diagonal = [grid[r][c + 2], grid[r + 1][c + 1], grid[r + 2][c]]

            if (''.join(main_diagonal).upper() in {"MAS", "SAM"}
                    and ''.join(anti_diagonal).upper() in {"MAS", "SAM"}):
                xmas_count += 1

    return xmas_count


def solve_part_1(input_string):
    grid = parse_input(input_string)
    return find_xmas_occurrences(grid)


def solve_part_2(input_string):
    grid = parse_input(input_string)
    return count_xmas_patterns(grid)


if __name__ == '__main__':
    input = get_puzzle_input(day=4)
    grid = parse_input(input)

    start_time = time.time()
    result_part_1 = find_xmas_occurrences(grid)
    execution_time = time.time() - start_time
    print(f"Puzzle result part 1 in {execution_time:.4f} seconds: {result_part_1}")

    start_time = time.time()
    result_part_2 = count_xmas_patterns(grid)
    execution_time = time.time() - start_time
    print(f"Puzzle result part 2 in {execution_time:.4f} seconds: {result_part_2}")
