from modules.data_processor import get_puzzle_input


def solve_part_1(input_str):
    # Parse input into grid and moves
    lines = input_str.strip().split('\n')

    # Find the empty line that separates grid and moves
    grid = []
    moves = ""
    parsing_moves = False
    for line in lines:
        if not line.strip():
            parsing_moves = True
            continue
        if parsing_moves:
            moves += line.strip()
        else:
            grid.append(list(line))

    # Find initial robot position
    robot_pos = None
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '@':
                robot_pos = (i, j)
                break
        if robot_pos:
            break

    # Direction mappings
    directions = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1)
    }

    # Process each move
    for move in moves:
        if move not in directions:
            continue

        dy, dx = directions[move]
        can_move = True
        boxes_to_move = []

        # Check if movement is possible and collect all boxes that need to be moved
        check_y, check_x = robot_pos[0] + dy, robot_pos[1] + dx
        while True:
            # Check if we're hitting a wall or out of bounds
            if (check_y < 0 or check_y >= len(grid) or
                    check_x < 0 or check_x >= len(grid[0]) or
                    grid[check_y][check_x] == '#'):
                can_move = False
                break

            # If we find empty space, we can stop checking
            if grid[check_y][check_x] == '.':
                break

            # If we find a box, add it to our list and continue checking
            if grid[check_y][check_x] == 'O':
                boxes_to_move.append((check_y, check_x))
                check_y += dy
                check_x += dx
                continue

            # If we find the robot, just continue
            if grid[check_y][check_x] == '@':
                check_y += dy
                check_x += dx
                continue

        # If movement is possible, update the grid
        if can_move:
            # Move all boxes
            if boxes_to_move:
                # Move boxes from back to front
                for box_y, box_x in reversed(boxes_to_move):
                    grid[box_y + dy][box_x + dx] = 'O'
                    grid[box_y][box_x] = '.'

            # Move robot
            new_y, new_x = robot_pos[0] + dy, robot_pos[1] + dx
            grid[new_y][new_x] = '@'
            grid[robot_pos[0]][robot_pos[1]] = '.'
            robot_pos = (new_y, new_x)

    # Calculate GPS coordinates
    total_gps = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'O':
                gps = 100 * i + j
                total_gps += gps

    return total_gps




if __name__ == '__main__':
    day = 15
    data = get_puzzle_input(day=day)

    result_part_1 = solve_part_1(data)
    print(f"Puzzle result part 1: {result_part_1}")

    result_part_2 = solve_part_2(data)
    print(f"Puzzle result part 2: {result_part_2}")
