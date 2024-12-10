import time
import sys

from modules.data_processor import get_puzzle_input

sys.setrecursionlimit(17500)

directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
direction_symbols = ['^', '>', 'v', '<']

marked_positions = []
marked_grid = [[]]

def get_grid(input_map):
    return [list(row) for row in input_map.splitlines()]


def find_starting_position(grid):
    rows, cols = len(grid), len(grid[0])

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] in direction_symbols:
                facing = direction_symbols.index(grid[r][c])
                return r, c, facing


def detect_loop(r_start, c_start, facing, r_obstruction, c_obstruction):
    global marked_grid, marked_positions

    rows, cols = len(marked_grid), len(marked_grid[0])

    guard_row, guard_col, guard_dir = r_start, c_start, facing

    visited = set()

    visited.add((guard_row, guard_col, guard_dir))

    while True:
        dr, dc = directions[guard_dir]
        nr, nc = guard_row + dr, guard_col + dc

        if (nr < 0 or nr >= rows or
                nc < 0 or nc >= cols):
            # running out of bounds
            return False

        # Check for obstacle
        is_obstacle = (
                (nr == r_obstruction and nc == c_obstruction) or
                marked_grid[nr][nc] == "#"
        )

        if is_obstacle:
            # Turn right
            guard_dir = (guard_dir + 1) % 4
        else:
            # Move forward
            guard_row, guard_col = nr, nc

            if marked_grid[guard_row][guard_col] != 'X':
                marked_grid[guard_row][guard_col] = 'X'
                marked_positions.append((guard_row, guard_col))

        state = (guard_row, guard_col, guard_dir)
        if state in visited:
            # Loop detected, already visited this place in the same direction
            return True

        visited.add(state)


def mark_grid(grid, r_start, c_start, facing):
    global marked_grid, marked_positions

    marked_grid = grid
    marked_positions = []

    rows, cols = len(grid), len(grid[0])
    r, c = r_start, c_start

    # Move until out of bounds
    while True:
        # Try to move forward
        dr, dc = directions[facing]
        nr, nc = r + dr, c + dc

        if (nr < 0 or nr >= rows or
                nc < 0 or nc >= cols):
            # running out of bounds
            break

        elif grid[nr][nc] == '#':
            # Turn right
            facing = (facing + 1) % 4

        else:
            r, c = nr, nc

            if marked_grid[r][c] != 'X':
                marked_grid[r][c] = 'X'  # Mark visited position
                marked_positions.append((r, c))


def solve_part_1(input_map):
    global marked_grid

    grid = get_grid(input_map)

    r, c, facing = find_starting_position(grid)

    grid[r][c] = 'X'  # Mark starting position

    mark_grid(grid, r, c, facing)

    return sum(row.count('X') for row in marked_grid)


def solve_part_2(input_map):
    """
    Thanks to @wijnand-gritter for the loop detector.
    """
    global marked_grid

    grid = get_grid(input_map)

    rows, cols = len(grid), len(grid[0])

    r_start, c_start, facing = find_starting_position(grid)
    mark_grid(grid, r_start, c_start, facing)

    valid_positions = 0
    checked_positions = 0

    for r in range(rows):
        for c in range(cols):
            checked_positions += 1

            # Skip obstacles and starting position
            if grid[r][c] == "#" or (r == r_start and c == c_start):
                continue

            # Loop with an obstruction at (r, c) ?
            if detect_loop(r_start, c_start, facing, r, c):
                valid_positions += 1

    return valid_positions


def dfs(grid, r, c, facing, r_obstruction, c_obstruction, visited):
    rows, cols = len(grid), len(grid[0])

    # Base cases
    if (r, c, facing) in visited:
        return True

    visited.add((r, c, facing))

    # Get next position
    dr, dc = directions[facing]
    nr, nc = r + dr, c + dc

    # Check bounds and obstacles
    if (nr < 0 or nr >= rows or nc < 0 or nc >= cols):
        return False

    # Check for obstacle (including artificial obstruction)
    if (nr == r_obstruction and nc == c_obstruction) or grid[nr][nc] == '#':
        # Turn right and continue from current position
        return dfs(grid, r, c, (facing + 1) % 4, r_obstruction, c_obstruction, visited)

    # Move forward
    return dfs(grid, nr, nc, facing, r_obstruction, c_obstruction, visited)


def get_initial_path(grid, r_start, c_start, facing):
    rows, cols = len(grid), len(grid[0])
    path = set()
    r, c = r_start, c_start

    while True:
        path.add((r, c))
        dr, dc = directions[facing]
        nr, nc = r + dr, c + dc

        if (nr < 0 or nr >= rows or nc < 0 or nc >= cols):
            break
        elif grid[nr][nc] == '#':
            facing = (facing + 1) % 4
        else:
            r, c = nr, nc

    return path


def solve_part_2_optimized(input_map):
    grid = get_grid(input_map)
    r_start, c_start, facing = find_starting_position(grid)

    # Get initial path without obstructions
    initial_path = get_initial_path(grid, r_start, c_start, facing)
    valid_positions = 0

    # Check each position in the initial path
    for r, c in initial_path:
        if grid[r][c] == '#' or (r == r_start and c == c_start):
            continue

        # Try to find a loop with obstruction at (r, c)
        if dfs(grid, r_start, c_start, facing, r, c, set()):
            valid_positions += 1

    return valid_positions

if __name__ == '__main__':
    day = 6
    data = get_puzzle_input(day=day)

    result_part_1 = solve_part_1(data)
    print(f"Puzzle result part 1: {result_part_1}")

    start_time = time.time()
    result_part_2 = solve_part_2(data)
    execution_time = time.time() - start_time
    print(f"Puzzle result part 2 brute force in {execution_time:.4}s: {result_part_2}")

    start_time = time.time()
    result_part_2 = solve_part_2_optimized(data)
    execution_time = time.time() - start_time

    print(f"Puzzle result part 2 optimized in {execution_time:.4}s: {result_part_2}")
