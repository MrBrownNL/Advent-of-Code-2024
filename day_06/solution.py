from modules.data_processor import get_puzzle_input


def solve_part_1(map_input):
    # Convert input to grid
    grid = [list(row) for row in map_input.splitlines()]

    # Directions: 0=North, 1=East, 2=South, 3=West
    dx = [-1, 0, 1, 0]
    dy = [0, 1, 0, -1]

    # Find initial guard position and direction
    rows, cols = len(grid), len(grid[0])
    x, y, facing = 0, 0, 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] in '^>v<':
                x, y = r, c
                facing = '^>v<'.index(grid[r][c])
                grid[r][c] = 'X'  # Mark starting position
                break
        else:
            continue
        break

    while True:
        # Try to move forward
        nx = x + dx[facing]
        ny = y + dy[facing]

        if (nx < 0 or nx >= rows or
                ny < 0 or ny >= cols):
            # running outside the grid
            break

        elif grid[nx][ny] == '#':
            # Turn right
            facing = (facing + 1) % 4

        else:
            x, y = nx, ny

            grid[x][y] = 'X'

    return sum(row.count('X') for row in grid)


def solve_part_2(input_map):
    pass


if __name__ == '__main__':
    day = 6
    data = get_puzzle_input(day=day)

    result_part_1 = solve_part_1(data)
    print(f"Puzzle result part 1: {result_part_1}")
    # submit_answer(answer=result_part_1, part=1, day=day)

    result_part_2 = solve_part_2(data)
    print(f"Puzzle result part 2: {result_part_2}")
    # submit_answer(answer=result_part_2, part=2, day=day)

