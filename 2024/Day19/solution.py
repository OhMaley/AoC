from functools import lru_cache
from typing import List, Tuple


def get_towels_and_designs_from_input_file(
    file_path: str,
) -> Tuple[List[str], List[str]]:
    with open(file_path, "r") as file:
        towels_str, designs_str = file.read().strip().split("\n\n")
        towel_patterns = towels_str.strip().split(", ")
        desired_designs = designs_str.strip().split("\n")
        return towel_patterns, desired_designs


@lru_cache(None)
def can_construct(remaining_target: str, towel_patterns: Tuple[str]) -> bool:
    if remaining_target == "":
        return True

    for pattern in towel_patterns:
        if remaining_target.startswith(pattern):
            if can_construct(remaining_target[len(pattern) :], towel_patterns):
                return True

    return False


@lru_cache(None)
def count_construct(remaining_target: str, towel_patterns: Tuple[str]) -> int:
    if remaining_target == "":
        return 1

    total_count = 0
    for pattern in towel_patterns:
        if remaining_target.startswith(pattern):
            total_count += count_construct(
                remaining_target[len(pattern) :], towel_patterns
            )

    return total_count


def get_nb_possible_designs(
    towel_patterns: List[str], desired_designs: List[str]
) -> int:
    return sum(
        1 if can_construct(design, tuple(towel_patterns)) else 0
        for design in desired_designs
    )


def count_total_different_ways(
    towel_patterns: List[str], desired_designs: List[str]
) -> int:
    return sum(
        count_construct(design, tuple(towel_patterns)) for design in desired_designs
    )


if __name__ == "__main__":
    towel_patterns, desired_designs = get_towels_and_designs_from_input_file(
        "./input.txt"
    )
    print(
        f"We have {len(towel_patterns)} towel patterns and we need to check {len(desired_designs)} desired designs"
    )

    nb_possible_designs = get_nb_possible_designs(towel_patterns, desired_designs)
    print(f"{nb_possible_designs} designs are possible")

    total_different_ways = count_total_different_ways(towel_patterns, desired_designs)
    print(
        f"The total number of different ways to make the designs is {total_different_ways}"
    )
