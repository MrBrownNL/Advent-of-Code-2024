from modules.data_processor import get_puzzle_input


def parse_disk_map(disk_map):
    result = []
    file_id = 0
    for i, count in enumerate(disk_map):
        count = int(count)
        if i % 2 == 0:
            result.extend([file_id] * count)
            file_id += 1
        else:
            result.extend(['.'] * count)
    return result

def compact_disk(disk):
    while '.' in disk:
        leftmost_free = disk.index('.')

        rightmost_file = -1
        rightmost_file_id = -1

        for i in range(len(disk)-1, -1, -1):
            if isinstance(disk[i], int):
                rightmost_file = i
                rightmost_file_id = disk[i]
                break

        if rightmost_file < leftmost_free:
            break

        disk[leftmost_free] = rightmost_file_id
        disk[rightmost_file] = '.'

    return disk


def compact_disk_optimized(disk):
    length = len(disk)
    # Pre-calculate file positions for faster lookup
    file_positions = {}
    for i in range(length - 1, -1, -1):
        if isinstance(disk[i], int):
            if disk[i] not in file_positions:
                file_positions[disk[i]] = []
            file_positions[disk[i]].append(i)

    # Find continuous spaces
    spaces = []
    current_space = []
    for i in range(length):
        if disk[i] == '.':
            current_space.append(i)
        elif current_space:
            spaces.append(current_space[:])
            current_space = []
    if current_space:
        spaces.append(current_space)

    # Process files from right to left
    for file_id in sorted(file_positions.keys(), reverse=True):
        positions = file_positions[file_id]
        if not positions:
            continue

        file_size = len(positions)

        # Find leftmost suitable space
        best_space = None
        for space in spaces:
            if len(space) >= file_size and space[0] < positions[0]:
                best_space = space
                break

        if best_space:
            # Move file
            for i in range(file_size):
                disk[best_space[i]] = file_id
                disk[positions[i]] = '.'

            # Update spaces
            spaces.remove(best_space)
            if len(best_space) > file_size:
                spaces.append(best_space[file_size:])

            new_space = positions
            spaces.append(new_space)
            spaces.sort(key=lambda x: x[0])

    return disk


def calculate_checksum(disk):
    # Use list comprehension and enumerate for better performance
    return sum(pos * block for pos, block in enumerate(disk) if isinstance(block, int))


def solve_part_1(disk_map):
    disk = parse_disk_map(disk_map)

    compacted_disk = compact_disk(disk)

    return calculate_checksum(compacted_disk)


def solve_part_2(disk_map):
    disk = parse_disk_map(disk_map)

    compacted_disk = compact_disk_optimized(disk)

    return calculate_checksum(compacted_disk)


if __name__ == '__main__':
    day = 9
    data = get_puzzle_input(day=day)

    result_part_1 = solve_part_1(data)
    print(f"Puzzle result part 1: {result_part_1}")

    result_part_2 = solve_part_2(data)
    print(f"Puzzle result part 2: {result_part_2}")
