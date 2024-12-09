from modules.data_processor import get_puzzle_input


def parse_disk_map(disk_map):
    position = 0
    file_id = 0
    disk = []

    for char in disk_map:
        if position % 2 == 0:
            character_to_add = file_id
            file_id += 1
        else:
            character_to_add = "."

        for i in range(int(char)):
            disk.append(character_to_add)

        position += 1

    return disk


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
    def get_most_right_file(start_index):
        right_most_file_start_index = -1
        file = []
        file_id = -1

        for i in range(start_index - 1, -1, -1):
            if isinstance(disk[i], int):
                if file_id == -1:
                    file_id = disk[i]

                if disk[i] == file_id:
                    file.append(disk[i])
                    right_most_file_start_index = i
            else:
                if file_id > -1:
                    break

        return right_most_file_start_index, file

    def get_left_most_free_space_for_file(file):
        space_needed = len(file)
        free_space = 0
        free_space_start_index = -1

        for i in range(len(disk) - 1):
            if isinstance(disk[i], str):
                if free_space_start_index == -1:
                    free_space_start_index = i
                free_space += 1

                if free_space == space_needed:
                    break
            else:
                free_space = 0
                free_space_start_index = -1

        return free_space_start_index

    def move_file(file, from_index, to_index):
        for i, file_id in enumerate(file):
            disk[to_index + i] = file_id
            disk[from_index + i] = '.'

    start_index = len(disk)
    while start_index > 1:
        from_index, file = get_most_right_file(start_index)
        to_index = get_left_most_free_space_for_file(file)

        if from_index > to_index:
            move_file(file, from_index, to_index)

        start_index = from_index

    return disk


def calculate_checksum(disk):
    checksum = 0
    for pos, block in enumerate(disk):
        if isinstance(block, int):
            checksum += pos * block
    return checksum

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
