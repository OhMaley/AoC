from typing import List, Tuple, Optional


def get_map_from_input(
    file_path: str, guard_possible_characters: str
) -> Optional[Tuple[List[str], Tuple[int, int], str]]:
    with open(file_path, "r") as file:
        complete_map = file.read().strip().split("\n")
        guard = find_char_in_map(complete_map, guard_possible_characters)
        if guard is None:
            return None
        i, j, c = guard
        complete_map[i] = complete_map[i][:j] + "." + complete_map[i][j + 1 :]
        return complete_map, (i, j), c


def find_char_in_map(grid: List[str], chars: str) -> Optional[Tuple[int, int, str]]:
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c in chars:
                return i, j, c
    return None


def guard_visited_cells(
    lab_map: List[str], guard_position: Tuple[int, int], guard_direction: str
) -> Tuple[List[List[List[str]]], bool]:
    height = len(lab_map)
    width = len(lab_map[0])
    visited = [[[] for _ in range(width)] for _ in range(height)]
    current_pos = guard_position
    current_dir = guard_direction
    rotate_char = {"^": ">", ">": "v", "v": "<", "<": "^"}

    while (
        current_pos[0] >= 0
        and current_pos[0] < height
        and current_pos[1] >= 0
        and current_pos[1] < width
        and current_dir not in visited[current_pos[0]][current_pos[1]]
    ):
        # Update the visited cells
        visited[current_pos[0]][current_pos[1]].append(current_dir)

        # Update the guard position or direction
        vector = (
            -1 if current_dir == "^" else 1 if current_dir == "v" else 0,
            -1 if current_dir == "<" else 1 if current_dir == ">" else 0,
        )
        next_pos = (current_pos[0] + vector[0], current_pos[1] + vector[1])
        if (
            next_pos[0] < 0
            or next_pos[0] >= height
            or next_pos[1] < 0
            or next_pos[1] >= width
        ):
            # Out of the map -> fake the next position
            current_pos = next_pos
        elif lab_map[next_pos[0]][next_pos[1]] == "#":
            # Hitting a wall -> only rotate by 90°
            current_dir = rotate_char[current_dir]
        else:
            # No wall -> move in the direction
            current_pos = next_pos

    # Count the visited cells:
    out_of_map = (
        current_pos[0] < 0
        or current_pos[0] >= height
        or current_pos[1] < 0
        or current_pos[1] >= height
    )
    in_loop = not out_of_map and current_dir in visited[current_pos[0]][current_pos[1]]
    return visited, in_loop


def count_possible_obstructions(
    lab_map: List[str],
    guard_position: Tuple[int, int],
    guard_direction: str,
    possible_positions: List[Tuple[int, int]],
) -> int:
    count = 0
    for pos in possible_positions:
        new_lab_map = list(lab_map)
        new_lab_map[pos[0]] = (
            new_lab_map[pos[0]][: pos[1]] + "#" + new_lab_map[pos[0]][pos[1] + 1 :]
        )
        _, in_loop = guard_visited_cells(new_lab_map, guard_position, guard_direction)
        if in_loop:
            count += 1
    return count


if __name__ == "__main__":
    guard_possible_characters = "^>v<"
    complete_map = get_map_from_input("./input.txt", guard_possible_characters)
    if complete_map:
        lab_map, guard_position, guard_direction = complete_map

        # Nb cells visited by the guard
        visited, in_loop = guard_visited_cells(lab_map, guard_position, guard_direction)
        nb_distinct_positions = sum(1 for row in visited for cell in row if cell)
        print(f"The guard visited {nb_distinct_positions} cells")

        # Nb possible obstructions to stuck the guard in a loop
        possible_positions = [
            (i, j)
            for i, row in enumerate(visited)
            for j, cell in enumerate(row)
            if cell and not (i == guard_position[0] and j == guard_position[1])
        ]
        nb_obstruction_positions = count_possible_obstructions(
            lab_map, guard_position, guard_direction, possible_positions
        )
        print(f"There are {nb_obstruction_positions} obstruction positions")
