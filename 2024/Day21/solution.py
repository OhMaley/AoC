import functools
from typing import List


grid_numbers = ["789", "456", "123", " 0A"]
grid_arrows = [" ^A", "<v>"]


def get_codes_from_input_file(file_path: str) -> List[str]:
    with open(file_path, "r") as file:
        return file.read().strip().splitlines()


def find_coordinates(grid, target):
    return next(
        (x, y)
        for y, row in enumerate(grid)
        for x, char in enumerate(row)
        if char == target
    )


def calculate_path(grid: List[str], start: str, end: str):
    start_x, start_y = find_coordinates(grid, start)
    end_x, end_y = find_coordinates(grid, end)

    def generate_path(x, y, current_path):
        if (x, y) == (end_x, end_y):
            yield current_path + "A"
        if end_x < x and grid[y][x - 1] != " ":
            yield from generate_path(x - 1, y, current_path + "<")
        if end_y < y and grid[y - 1][x] != " ":
            yield from generate_path(x, y - 1, current_path + "^")
        if end_y > y and grid[y + 1][x] != " ":
            yield from generate_path(x, y + 1, current_path + "v")
        if end_x > x and grid[y][x + 1] != " ":
            yield from generate_path(x + 1, y, current_path + ">")

    # Select the path with the fewest direction changes
    return min(
        generate_path(start_x, start_y, ""),
        key=lambda path: sum(a != b for a, b in zip(path, path[1:])),
    )


@functools.cache
def compute_sequence(sequence: str, level: int, max_level: int) -> int:
    if level > max_level:
        return len(sequence)
    grid = grid_arrows if level else grid_numbers
    return sum(
        compute_sequence(calculate_path(grid, from_char, to_char), level + 1, max_level)
        for from_char, to_char in zip("A" + sequence, sequence)
    )


def compute_complexity(code: str, nb_robots: int) -> int:
    seq_len = compute_sequence(code, 0, nb_robots)
    num_part = int("".join(x for x in code if x.isdigit()))
    print(
        f"Code {code} has a sequence of length {seq_len} and has a numerical part of {num_part} for a total of {seq_len * num_part}"
    )
    return seq_len * num_part


if __name__ == "__main__":
    codes = get_codes_from_input_file("./input.txt")
    print(f"codes = {codes}")

    # Find sum of the complexities with 2 robots
    complexities = [compute_complexity(code, 2) for code in codes]
    total = sum(complexities)
    print(f"The sum of the complexities of the codes is {total}")

    # Find sum of the complexities with 25 robots
    complexities = [compute_complexity(code, 25) for code in codes]
    total = sum(complexities)
    print(f"The sum of the complexities of the codes is {total}")
