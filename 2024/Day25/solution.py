from itertools import product
from typing import List, Tuple


def get_heights(pattern: str) -> List[int]:
    rows = pattern.splitlines()
    num_columns = max(len(row) for row in rows)
    column_counts = [-1] * num_columns
    for row in rows:
        for i, char in enumerate(row):
            if char == "#":
                column_counts[i] += 1
    return column_counts


def get_keys_and_locks_from_input_file(
    file_path: str,
) -> Tuple[List[List[int]], List[List[int]], int]:
    with open(file_path, "r") as file:
        entities = file.read().strip().split("\n\n")
        keys = []
        locks = []
        heights = []
        for entity in entities:
            lines = entity.strip().splitlines()
            if all(char == "#" for char in lines[0]) and all(
                char == "." for char in lines[-1]
            ):
                locks.append(get_heights(entity))
                heights.append(len(lines))
            elif all(char == "." for char in lines[0]) and all(
                char == "#" for char in lines[-1]
            ):
                keys.append(get_heights(entity))
                heights.append(len(lines))
            else:
                print("!!!!!!!!!!!!! NOT a KEY OR A LOCK !!!!!!!!!!!!!")

        if len(set(heights)) != 1:
            raise Exception("Different heights not allowed !")

        return keys, locks, heights[0] - 1


def is_pair_working(key: List[int], lock: List[int], height: int) -> bool:
    return all(x + y < height for x, y in zip(key, lock))


def get_key_lock_working_combination(
    keys: List[List[int]], locks: List[List[int]], height: int
) -> int:
    total = 0
    for pair in product(keys, locks):
        key, lock = pair
        if is_pair_working(key, lock, height):
            total += 1
    return total


if __name__ == "__main__":
    # Get the locks and the keys from the file
    keys, locks, height = get_keys_and_locks_from_input_file("./input.txt")

    # Display some information
    nb_keys = len(keys)
    nb_locks = len(locks)
    nb_possible_key_lock_combination = nb_keys * nb_locks
    print(f"Got {nb_keys} keys and {nb_locks} locks of height {height}")
    print(f"There are {nb_possible_key_lock_combination} possible combinations")

    # Check the number of key / lock pair that fit together
    nb_working_pairs = get_key_lock_working_combination(keys, locks, height)
    print(f"There are {nb_working_pairs} lock/key pairs that fit together")
