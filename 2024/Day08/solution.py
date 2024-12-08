from typing import List, Dict, Tuple, Set, Optional
from collections import defaultdict
from itertools import combinations


def get_antennas_map_from_input_file(file_path: str) -> List[str]:
    with open(file_path, "r") as file:
        return file.read().strip().split("\n")


def extract_antennas_positions_from_map(
    antennas_map: List[str],
) -> Dict[str, List[Tuple[int, int]]]:
    antennas_positions: Dict[str, List[Tuple[int, int]]] = defaultdict(list)
    for i, row in enumerate(antennas_map):
        for j, c in enumerate(row):
            if c.isalpha() or c.isdigit():
                antennas_positions[c].append((i, j))

    return antennas_positions


def get_antinodes_positions(
    antennas_positions: Dict[str, List[Tuple[int, int]]],
    height: int,
    width: int,
    with_harmonics: bool,
) -> Set[Tuple[int, int]]:
    unique_positions = set()
    for positions in antennas_positions.values():
        for p1, p2 in combinations(positions, 2):
            harmonics = get_harmonics(
                p1, p2, [1] if not with_harmonics else None, height, width
            )
            unique_positions.update(harmonics)

    return unique_positions


def get_harmonics(
    p1: Tuple[int, int],
    p2: Tuple[int, int],
    harmonic_numbers: Optional[List[int]],
    height: int,
    width: int,
) -> Set[Tuple[int, int]]:
    harmonics = set()

    # Vectors
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]

    if harmonic_numbers:
        for i in harmonic_numbers:
            p3 = (p2[0] + i * dx, p2[1] + i * dy)
            p4 = (p1[0] - i * dx, p1[1] - i * dy)
            if p3[0] >= 0 and p3[0] < height and p3[1] >= 0 and p3[1] < width:
                harmonics.add((p3[0], p3[1]))
            if p4[0] >= 0 and p4[0] < height and p4[1] >= 0 and p4[1] < width:
                harmonics.add((p4[0], p4[1]))
    else:
        # One direction
        i = 0
        in_bounds = True
        while in_bounds:
            p = (p2[0] + i * dx, p2[1] + i * dy)
            if p[0] >= 0 and p[0] < height and p[1] >= 0 and p[1] < width:
                harmonics.add((p[0], p[1]))
            else:
                in_bounds = False
            i += 1

        # Other direction
        i = 0
        in_bounds = True
        while in_bounds:
            p = (p1[0] - i * dx, p1[1] - i * dy)
            if p[0] >= 0 and p[0] < height and p[1] >= 0 and p[1] < width:
                harmonics.add((p[0], p[1]))
            else:
                in_bounds = False
            i += 1

    return harmonics


if __name__ == "__main__":
    antennas_map = get_antennas_map_from_input_file("./input.txt")
    height = len(antennas_map)
    width = len(antennas_map[0])
    antennas_positions = extract_antennas_positions_from_map(antennas_map)

    # Antinodes
    antinodes_positions = get_antinodes_positions(
        antennas_positions, height, width, False
    )
    print(f"The number of unique antinodes positions is {len(antinodes_positions)}")

    # Antinodes with harmonics
    antinodes_positions = get_antinodes_positions(
        antennas_positions, height, width, True
    )
    print(f"The number of unique antinodes positions is {len(antinodes_positions)}")
