from data_retriever import get_puzzle_input

def calculate_similarity_score(left_list, right_list):
    right_count = {}
    for num in right_list:
        right_count[num] = right_count.get(num, 0) + 1

    similarity_score = 0
    for num in left_list:
        count = right_count.get(num, 0)
        similarity_score += num * count

    return similarity_score


def main():
    left_list, right_list = get_puzzle_input()
    similarity_score = calculate_similarity_score(left_list, right_list)
    print(f"Similarity score: {similarity_score}")

if __name__ == "__main__":
    main()
