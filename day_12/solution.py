from modules.data_processor import get_puzzle_input


def parse_input(puzzle_input):
    return list(map(int, puzzle_input.strip().split()))


def solve_part_1(grid: list[list]) -> int:
    rows, cols = len(grid), len(grid[0])
    visited = set()
    total_price = 0

    def get_region(r: int, c: int, plant: str) -> tuple[int, int]:
        if (r < 0 or r >= rows or c < 0 or c >= cols or
                (r, c) in visited or grid[r][c] != plant):
            return 0, 0

        visited.add((r, c))
        area = 1
        perimeter = 0

        # Calculate perimeter
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if (nr < 0 or nr >= rows or nc < 0 or nc >= cols or
                    grid[nr][nc] != plant):
                perimeter += 1

        # Find connected plots
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            sub_area, sub_perimeter = get_region(nr, nc, plant)
            area += sub_area
            perimeter += sub_perimeter

        return area, perimeter

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                area, perimeter = get_region(r, c, grid[r][c])
                total_price += area * perimeter

    return total_price


def solve_part_2(input):
    pass


if __name__ == '__main__':
    day = 12
    data = get_puzzle_input(day=day)
    grid = [list(line) for line in data.strip().split('\n')]

    result_part_1 = solve_part_1(grid)
    print(f"Puzzle result part 1: {result_part_1}")

    result_part_2 = solve_part_2(grid)
    print(f"Puzzle result part 2: {result_part_2}")
