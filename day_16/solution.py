from modules.data_processor import get_puzzle_input
from dataclasses import dataclass
from typing import Tuple
import heapq
from heapq import heappop, heappush
from collections import defaultdict, deque
import math


@dataclass(frozen=True)
class State:
    x: int
    y: int
    direction: Tuple[int, int]

    def __lt__(self, other):
        # This is needed for the priority queue
        # The actual comparison doesn't matter since we're using the score as the primary key
        return False


def solve_part_1(input_data: str) -> int:
    # Parse the maze
    maze = input_data.strip().split('\n')
    height = len(maze)
    width = len(maze[0])

    # Find start and end positions
    start_pos = None
    end_pos = None
    for y in range(height):
        for x in range(width):
            if maze[y][x] == 'S':
                start_pos = (x, y)
            elif maze[y][x] == 'E':
                end_pos = (x, y)

    # Directions: (dx, dy) - East, North, West, South
    directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]

    # Initialize priority queue and visited dictionary
    # Format: (score, State)
    pq = [(0, State(start_pos[0], start_pos[1], (1, 0)))]  # Start facing East
    visited = {}  # State -> best_score

    while pq:
        score, state = heapq.heappop(pq)

        # Check if we reached the end
        if (state.x, state.y) == end_pos:
            return score

        # Skip if we've been here in this direction with a better score
        if state in visited and visited[state] <= score:
            continue
        visited[state] = score

        # Try all possible moves from current position

        # Move forward
        new_x = state.x + state.direction[0]
        new_y = state.y + state.direction[1]
        if (0 <= new_x < width and 0 <= new_y < height and
                maze[new_y][new_x] != '#'):
            new_state = State(new_x, new_y, state.direction)
            new_score = score + 1
            if new_state not in visited or new_score < visited[new_state]:
                heapq.heappush(pq, (new_score, new_state))

        # Turn left (counterclockwise)
        idx = directions.index(state.direction)
        new_dir = directions[(idx + 1) % 4]
        new_state = State(state.x, state.y, new_dir)
        new_score = score + 1000
        if new_state not in visited or new_score < visited[new_state]:
            heapq.heappush(pq, (new_score, new_state))

        # Turn right (clockwise)
        new_dir = directions[(idx - 1) % 4]
        new_state = State(state.x, state.y, new_dir)
        new_score = score + 1000
        if new_state not in visited or new_score < visited[new_state]:
            heapq.heappush(pq, (new_score, new_state))

    return float('inf')


def parse_maze(maze_str):
    lines = maze_str.strip().split('\n')
    maze = {}
    start = None
    end = None

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != '#':
                maze[(x, y)] = char
                if char == 'S':
                    start = (x, y)
                elif char == 'E':
                    end = (x, y)

    return maze, start, end


def a_star(maze, start, end):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Up, Right, Down, Left
    initial_dir = 1  # Start facing East

    queue = [(0, start, initial_dir, 0)]  # (priority, pos, direction, cost)
    costs = defaultdict(lambda: math.inf)
    costs[(start, initial_dir)] = 0
    predecessors = defaultdict(set)

    while queue:
        _, current_pos, current_dir, current_cost = heappop(queue)

        # Skip if we've found a better path to this state
        if current_cost > costs[(current_pos, current_dir)]:
            continue

        for new_dir, (dx, dy) in enumerate(directions):
            next_pos = (current_pos[0] + dx, current_pos[1] + dy)

            if next_pos not in maze:
                continue

            turn_cost = 1000 if new_dir != current_dir else 0
            new_cost = current_cost + 1 + turn_cost

            if new_cost <= costs[(next_pos, new_dir)]:
                if new_cost < costs[(next_pos, new_dir)]:
                    costs[(next_pos, new_dir)] = new_cost
                    predecessors[(next_pos, new_dir)] = set()
                    priority = new_cost + manhattan_distance(next_pos, end)
                    heappush(queue, (priority, next_pos, new_dir, new_cost))
                predecessors[(next_pos, new_dir)].add((current_pos, current_dir))

    return costs, predecessors


def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def find_best_paths(maze, start, end, costs, predecessors):
    # Find the minimum cost to reach the end
    min_cost = math.inf
    for dir in range(4):
        cost = costs[(end, dir)]
        if cost < min_cost:
            min_cost = cost

    # Use BFS to find all tiles in optimal paths
    visited = set()
    queue = [(end, dir) for dir in range(4) if costs[(end, dir)] == min_cost]
    best_tiles = {end}

    while queue:
        current = queue.pop(0)
        if current in visited:
            continue

        visited.add(current)
        current_pos, _ = current
        best_tiles.add(current_pos)

        # Add all predecessors that lead to optimal paths
        for pred in predecessors[current]:
            if costs[pred] + (1000 if pred[1] != current[1] else 0) + 1 == costs[current]:
                if pred not in visited:
                    queue.append(pred)

    return best_tiles


def solve_part_2(input_str):
    maze, start, end = parse_maze(input_str)
    costs, predecessors = a_star(maze, start, end)
    best_tiles = find_best_paths(maze, start, end, costs, predecessors)
    return len(best_tiles)


if __name__ == '__main__':
    day = 16
    data = get_puzzle_input(day=day)

    result_part_1 = solve_part_1(data)
    print(f"Puzzle result part 1: {result_part_1}")

    result_part_2 = solve_part_2(data)
    print(f"Puzzle result part 2: {result_part_2}")
