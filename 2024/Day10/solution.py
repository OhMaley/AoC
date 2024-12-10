from typing import List, Dict, Tuple
from collections import deque


def get_topographic_map_from_input_file(file_path: str) -> List[List[int]]:
    with open(file_path, "r") as file:
        return [[int(x) for x in line] for line in file.read().strip().split("\n")]


def bfs(start_row: int, start_col: int, grid: List[List[int]], directions) -> int:
    height = len(grid)
    width = len(grid[0])
    queue = deque([(start_row, start_col, 0)])
    visited = set()
    visited.add((start_row, start_col))
    reachable_nines = set()

    while queue:
        i, j, value = queue.popleft()

        for di, dj in directions:
            neighbor_i, neighbor_j = i + di, j + dj

            if 0 <= neighbor_i < height and 0 <= neighbor_j < width:
                if (
                    grid[neighbor_i][neighbor_j] == value + 1
                    and (neighbor_i, neighbor_j) not in visited
                ):
                    if grid[neighbor_i][neighbor_j] == 9:
                        reachable_nines.add((neighbor_i, neighbor_j))
                    else:
                        queue.append(
                            (neighbor_i, neighbor_j, grid[neighbor_i][neighbor_j])
                        )
                    visited.add((neighbor_i, neighbor_j))

    return len(reachable_nines)


def dfs(row: int, col: int, grid: List[List[int]], directions, visited) -> int:
    if grid[row][col] == 9:
        return 1

    height = len(grid)
    width = len(grid[0])
    visited.add((row, col))
    total_paths = 0

    for di, dj in directions:
        neighbor_i, neighbor_j = row + di, col + dj
        if 0 <= neighbor_i < height and 0 <= neighbor_j < width:
            if (
                grid[neighbor_i][neighbor_j] == grid[row][col] + 1
                and (neighbor_i, neighbor_j) not in visited
            ):
                total_paths += dfs(neighbor_i, neighbor_j, grid, directions, visited)

    visited.remove((row, col))
    return total_paths


def get_trailheads_scores(
    topographic_map: List[List[int]],
) -> Dict[Tuple[int, int], int]:
    trailheads_scores = {}
    height = len(topographic_map)
    width = len(topographic_map[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    zeros_positions = [
        (i, j)
        for i in range(height)
        for j in range(width)
        if topographic_map[i][j] == 0
    ]

    for i, j in zeros_positions:
        trailheads_scores[(i, j)] = bfs(i, j, topographic_map, directions)

    return trailheads_scores


def get_trailheads_ratings(
    topographic_map: List[List[int]],
) -> Dict[Tuple[int, int], int]:
    trailheads_ratings = {}
    height = len(topographic_map)
    width = len(topographic_map[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    zeros_positions = [
        (i, j)
        for i in range(height)
        for j in range(width)
        if topographic_map[i][j] == 0
    ]

    for i, j in zeros_positions:
        trailheads_ratings[(i, j)] = dfs(i, j, topographic_map, directions, set())
    return trailheads_ratings


if __name__ == "__main__":
    topographic_map = get_topographic_map_from_input_file("./input.txt")

    trailhead_scores = get_trailheads_scores(topographic_map)
    total_score = sum(trailhead_scores.values())
    print(f"The sum of the scores of all trailheads is {total_score}")

    trailhead_ratings = get_trailheads_ratings(topographic_map)
    total_ratings = sum(trailhead_ratings.values())
    print(f"The sum of the ratings of all trailheads is {total_ratings}")
