from modules.data_processor import get_puzzle_input

def solve_part_1(puzzle_input):
    lines = puzzle_input.strip().split('\n')
    height = len(lines)
    width = len(lines[0])

    antenna_positions = {}
    for y in range(height):
        for x in range(width):
            char = lines[y][x]
            if char.isalnum():
                if char not in antenna_positions:
                    antenna_positions[char] = []
                antenna_positions[char].append((x, y))

    antinode_locations = set()

    for frequency, positions in antenna_positions.items():
        n = len(positions)
        for i in range(n):
            for j in range(i + 1, n):
                x1, y1 = positions[i]
                x2, y2 = positions[j]

                # Calculate potential antinodes
                dx, dy = x2 - x1, y2 - y1

                # Antinode 1 (twice the distance in the direction of the vector)
                antinode1_x = x1 - dx
                antinode1_y = y1 - dy

                # Antinode 2 (twice the distance in the opposite direction)
                antinode2_x = x2 + dx
                antinode2_y = y2 + dy

                if 0 <= antinode1_x < width and 0 <= antinode1_y < height:
                    antinode_locations.add((antinode1_x, antinode1_y))

                if 0 <= antinode2_x < width and 0 <= antinode2_y < height:
                    antinode_locations.add((antinode2_x, antinode2_y))

    return len(antinode_locations)


def solve_part_2(input_map):
    grid = [list(line) for line in input_map.strip().split('\n')]

    antennas = {}
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell.isalnum():
                if cell not in antennas:
                    antennas[cell] = []
                antennas[cell].append((x, y))

    antinodes = set()

    for freq, locations in antennas.items():
        for i, (x1, y1) in enumerate(locations):
            for j, (x2, y2) in enumerate(locations):
                if i == j:
                    continue

                # Calculate the direction vector
                dx = x2 - x1
                dy = y2 - y1

                # Find antinodes along this line
                for k in range(-len(grid[0]), len(grid[0])):
                    ax = x1 + k * dx
                    ay = y1 + k * dy

                    # Check if this antinode is within the grid bounds
                    if (0 <= ax < len(grid[0]) and 0 <= ay < len(grid)):
                        antinodes.add((ax, ay))

    return len(antinodes)


if __name__ == '__main__':
    day = 8
    data = get_puzzle_input(day=day)

    result_part_1 = solve_part_1(data)
    print(f"Puzzle result part 1: {result_part_1}")
    # submit_answer(answer=result_part_1, part=1, day=day)

    result_part_2 = solve_part_2(data)
    print(f"Puzzle result part 2: {result_part_2}")
    # # submit_answer(answer=result_part_2, part=2, day=day)
