from typing import List, Tuple, Optional
import functools


def get_stones_from_input_file(file_path: str) -> List[int]:
    with open(file_path, "r") as file:
        return [int(n) for n in file.read().strip().split(" ")]


def count_stones_after_blinks(stones: List[int], nb_blinks: int) -> int:
    return sum([count_single_stone_after_blinks(stone, nb_blinks) for stone in stones])


@functools.lru_cache(maxsize=None)
def count_single_stone_after_blinks(stone: int, depth: int) -> int:
    # Blink
    left_stone, right_stone = blink_single_stone(stone)

    # Last iteration
    if depth == 1:
        return 1 if right_stone is None else 2

    # Recurse
    count = count_single_stone_after_blinks(left_stone, depth - 1)
    if right_stone is not None:
        count += count_single_stone_after_blinks(right_stone, depth - 1)

    return count


@functools.lru_cache(maxsize=None)
def blink_single_stone(stone: int) -> Tuple[int, Optional[int]]:
    # Rule 1
    if stone == 0:
        return (1, None)

    # Rule 2
    stone_str = str(stone)
    nb_digits = len(stone_str)
    if nb_digits % 2 == 0:
        split_index = nb_digits // 2
        left_stone = int(stone_str[:split_index])
        right_stone = int(stone_str[split_index:])
        return (left_stone, right_stone)

    # Rule 3
    return (stone * 2024, None)


if __name__ == "__main__":
    stones = get_stones_from_input_file("./input.txt")

    # 25 blinks
    nb_blinks = 25
    number_of_stones = count_stones_after_blinks(stones, nb_blinks)
    print(f"After {nb_blinks} blinks we will have {number_of_stones} stones")

    # 75 blinks
    nb_blinks = 75
    number_of_stones = count_stones_after_blinks(stones, nb_blinks)
    print(f"After {nb_blinks} blinks we will have {number_of_stones} stones")
