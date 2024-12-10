from modules.data_processor import get_puzzle_input


grid = [[]]

def get_map(input_map):
    global grid
    grid = [list(map(int, line)) for line in input_map.strip().split('\n')]



def get_trail_head_scores(start_r: int, start_c: int) -> tuple[int, int]:
    visited = set()
    valid_trails = set()
    distinct_paths = 0

    def dfs(r: int, c: int, current_height: int) -> None:
        nonlocal distinct_paths

        if (r, c) in visited or not (0 <= r < len(grid) and 0 <= c < len(grid[0])):
            return
        if grid[r][c] != current_height:
            return
        if current_height == 9:
            valid_trails.add((r, c))
            distinct_paths += 1
            return

        visited.add((r, c))

        for nr, nc in [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]:
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                dfs(nr, nc, current_height + 1)

        visited.remove((r, c))

    dfs(start_r, start_c, 0)

    return len(valid_trails), distinct_paths


def solve_puzzle(input):
    get_map(input)
    total_score = 0
    total_rating = 0

    rows, cols = len(grid), len(grid[0])

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                score, rating = get_trail_head_scores(r, c)
                total_score += score
                total_rating += rating

    return total_score, total_rating


def solve_part_1(input):
    total_score, total_rating = solve_puzzle(input)

    return total_score


def solve_part_2(input):
    total_score, total_rating = solve_puzzle(input)

    return total_rating


if __name__ == '__main__':
    day = 10
    data = get_puzzle_input(day=day)

    result_part_1 = solve_part_1(data)
    print(f"Puzzle result part 1: {result_part_1}")

    result_part_2 = solve_part_2(data)
    print(f"Puzzle result part 2: {result_part_2}")
