from data_retriever import get_puzzle_input

def calculate_total_distance(left_list, right_list):
    left_sorted = sorted(left_list)
    right_sorted = sorted(right_list)

    distances = [abs(left - right) for left, right in zip(left_sorted, right_sorted)]

    return sum(distances)

def main():
    left_list, right_list = get_puzzle_input()

    total_distance = calculate_total_distance(left_list, right_list)

    print(f"Total distance: {total_distance}")

if __name__ == "__main__":
    main()
