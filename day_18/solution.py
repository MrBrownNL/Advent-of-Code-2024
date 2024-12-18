from modules.data_processor import get_puzzle_input
from collections import deque


def parse_input(data):
    coordinates = []
    for line in data.strip().split('\n'):
        x, y = map(int, line.split(','))
        coordinates.append((x, y))

    return coordinates


def solve_part_1(input_data: str) -> int:
    size = 70
    start_position = (0, 0)
    finish_position = (size, size)
    corrupted = set()

    coordinates = parse_input(input_data)

    # only use the first 1024 'bytes'
    for x, y in coordinates[:1024]:
        corrupted.add((x, y))

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    queue = deque([(start_position, 0)])

    visited = set()
    visited.add(start_position)

    while queue:
        (x, y), dist = queue.popleft()

        if (x, y) == finish_position:
            return dist

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            new_pos = (nx, ny)

            if (0 <= nx < (size + 1) and
                    0 <= ny < (size + 1) and
                    new_pos not in corrupted and
                    new_pos not in visited):
                queue.append((new_pos, dist + 1))
                visited.add(new_pos)

    # queue empty, no path possible
    return -1


def solve_part_2(input_data: str):
    size = 70

    coordinates = parse_input(input_data)

    def has_path(corrupted):
        queue = deque([(0, 0)])  # Start position
        visited = {(0, 0)}

        # Directions: right, down, left, up
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        while queue:
            x, y = queue.popleft()

            if (x, y) == (size, size):
                return True

            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy

                if (0 <= new_x <= size and
                        0 <= new_y <= size and
                        (new_x, new_y) not in corrupted and
                        (new_x, new_y) not in visited):
                    visited.add((new_x, new_y))
                    queue.append((new_x, new_y))

        return False

    left, right = 0, len(coordinates) - 1

    while left < right:
        mid = (left + right) // 2
        corrupted = set(coordinates[:mid+1])

        if has_path(corrupted):
            left = mid + 1
        else:
            right = mid

    blocking_x, blocking_y = coordinates[left]
    return f"{blocking_x},{blocking_y}"


if __name__ == '__main__':
    day = 18
    data = get_puzzle_input(day=day)

    result_part_1 = solve_part_1(data)
    print(f"Puzzle result part 1: {result_part_1}")

    result_part_2 = solve_part_2(data)
    print(f"Puzzle result part 2: {result_part_2}")
