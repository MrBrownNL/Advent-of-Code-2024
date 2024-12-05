from data_processor import get_puzzle_input, submit_answer


def parse_input(input_string):
    """
    Parses the input string into ordering rules and updates.

    Args:
    - input_string (str): The input string containing rules and updates.

    Returns:
    - Tuple[List[Tuple[int, int]], List[List[int]]]:
        - rules: A list of tuples representing page ordering constraints.
        - updates: A list of lists of page numbers to validate.
    """
    sections = input_string.strip().split('\n\n')

    rules = [
        tuple(map(int, line.split('|')))
        for line in sections[0].split('\n')
        if '|' in line
    ]

    updates = [
        list(map(int, line.split(',')))
        for line in sections[1].split('\n')
    ]

    return rules, updates


def is_update_valid(update, rules):
    """
    Determines if an update is valid based on given rules.

    Args:
    - update (List[int]): List of page numbers in the current order.
    - rules (List[Tuple[int, int]]): Page ordering constraints.

    Returns:
    - bool: True if the update is valid, False otherwise.
    """
    relevant_rules = [
        (before, after) for before, after in rules
        if before in update and after in update
    ]

    for before, after in relevant_rules:
        if update.index(before) > update.index(after):
            return False

    return True


def build_dependency_graph(update, rules):
    """
    Builds a dependency graph for the given update based on rules.

    Args:
    - update (List[int]): List of page numbers in the current order.
    - rules (List[Tuple[int, int]]): Page ordering constraints.

    Returns:
    - Dict[int, Set[int]]: Dependency graph for the update.
    """
    graph = {page: set() for page in update}

    for before, after in rules:
        if before in update and after in update:
            graph[before].add(after)

    return graph


def topological_sort(graph, update):
    """
    Performs a topological sort on the dependency graph.

    Args:
    - graph (Dict[int, Set[int]]): Dependency graph.
    - update (List[int]): List of page numbers.

    Returns:
    - List[int]: A list of pages sorted according to dependencies.
    """
    visited = set()
    result = []

    def depth_first_search(node):
        if node in visited:
            return
        visited.add(node)
        for neighbor in graph[node]:
            depth_first_search(neighbor)
        result.append(node)

    for page in update:
        if page not in visited:
            depth_first_search(page)

    return list(reversed(result))


def correct_update_order(update, rules):
    """
    Corrects the order of an update based on given rules.

    Args:
    - update (List[int]): List of page numbers in the current order.
    - rules (List[Tuple[int, int]]): Page ordering constraints.

    Returns:
    - List[int]: Correctly ordered list of page numbers.
    """
    graph = build_dependency_graph(update, rules)
    return topological_sort(graph, update)


def get_middle_page(update):
    """
    Finds the middle page of an update.

    Args:
    - update (List[int]): List of page numbers.

    Returns:
    - int: The middle page number.
    """
    mid_index = len(update) // 2
    return update[mid_index]


def solve_puzzle_1(input_string):
    """
    Solves the puzzle by validating updates and summing their middle pages.

    Args:
    - input_string (str): The input string containing rules and updates.

    Returns:
    - int: Sum of middle pages from valid updates.
    """
    rules, updates = parse_input(input_string)
    valid_middle_pages = [
        get_middle_page(update)
        for update in updates
        if is_update_valid(update, rules)
    ]
    return sum(valid_middle_pages)


def solve_puzzle_2(input_string):
    """
    Solves the puzzle by correcting updates and summing their middle pages.

    Args:
    - input_string (str): The input string containing rules and updates.

    Returns:
    - int: Sum of middle pages from corrected updates.
    """
    rules, updates = parse_input(input_string)
    corrected_middle_pages = [
        get_middle_page(correct_update_order(update, rules))
        for update in updates
        if not is_update_valid(update, rules)
    ]
    return sum(corrected_middle_pages)


if __name__ == '__main__':
    day = 5
    data = get_puzzle_input(day=day)

    result_part_1 = solve_puzzle_1(data)
    print(f"Puzzle result part 1: {result_part_1}")
    submit_answer(answer=result_part_1, part=1, day=day)

    result_part_2 = solve_puzzle_2(data)
    print(f"Puzzle result part 2: {result_part_2}")
    submit_answer(answer=result_part_2, part=2, day=day)
