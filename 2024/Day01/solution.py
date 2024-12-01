from typing import List, Tuple
from collections import Counter


def get_lists_from_input_file(file_path: str) -> Tuple[List[int], List[int]]:
    left_list: List[int] = []
    right_list: List[int] = []

    with open(file_path, "r") as file:
        lines = file.read().strip().split("\n")

        for line in lines:
            left_location_id, right_location_id = map(int, line.split())
            left_list.append(left_location_id)
            right_list.append(right_location_id)

    return left_list, right_list


def get_total_distance(list1: List[int], list2: List[int]) -> int:
    return sum(abs(a - b) for a, b in zip(list1, list2))


def get_similarity_score(list1: List[int], list2: List[int]) -> int:
    occurrences = Counter(list2)
    return sum(num * occurrences[num] for num in list1)


if __name__ == "__main__":
    left_list, right_list = get_lists_from_input_file("./input.txt")

    left_list.sort()
    right_list.sort()

    total_distance = get_total_distance(left_list, right_list)
    print(f"The total distance between the two lists is {total_distance}")

    similarity_score = get_similarity_score(left_list, right_list)
    print(f"The similarity score between the two lists is {similarity_score}")
