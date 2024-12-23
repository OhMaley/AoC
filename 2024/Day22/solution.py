from collections import defaultdict
from itertools import pairwise
from typing import List, Tuple, Dict


def get_secret_numbers_from_input_file(file_path: str) -> List[int]:
    with open(file_path, "r") as file:
        return [int(line.strip()) for line in file.readlines()]


def compute_next_number(s: int) -> int:
    # 3-steps binary transformations
    s = (s ^ (s << 6)) & 0xFFFFFF
    s = (s ^ (s >> 5)) & 0xFFFFFF
    return (s ^ (s << 11)) & 0xFFFFFF


def generate_number_sequence(start: int, count: int) -> List[int]:
    sequence = [start]
    current = start
    for _ in range(count):
        current = compute_next_number(current)
        sequence.append(current)
    return sequence


def calculate_differences(sequence: List[int]) -> List[int]:
    return [b % 10 - a % 10 for a, b in pairwise(sequence)]


def compute_most_common_patterns(
    sequences: List[List[int]], pattern_length: int = 4
) -> Tuple[int, int]:
    total_sum = sum(seq[-1] for seq in sequences)
    pattern_counts: Dict[Tuple[int, ...], int] = defaultdict(int)

    for sequence in sequences:
        differences = calculate_differences(sequence)
        seen_patterns = set()

        for i in range(len(sequence) - pattern_length):
            pattern = tuple(differences[i : i + pattern_length])
            if pattern not in seen_patterns:
                pattern_counts[pattern] += sequence[i + pattern_length] % 10
                seen_patterns.add(pattern)

    max_pattern_value = max(pattern_counts.values())
    return total_sum, max_pattern_value


if __name__ == "__main__":
    # Load initial values from the input file
    initial_numbers = get_secret_numbers_from_input_file("input.txt")

    # Generate sequences for each initial number
    sequences = [generate_number_sequence(num, 2000) for num in initial_numbers]

    # Compute results
    total, max_pattern_value = compute_most_common_patterns(sequences)
    print(f"The total sum of the 2000th number in each sequence is: {total}")
    print(f"The most number of bananas I can get is {max_pattern_value}")
