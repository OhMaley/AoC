from typing import List, Tuple, Set


def get_garden_from_input_file(file_path: str) -> List[List[str]]:
    with open(file_path, "r") as file:
        return [list(line) for line in file.read().strip().split("\n")]


def flood_fill(start, garden, directions, visited):
    height, width = len(garden), len(garden[0])
    queue = [start]
    visited[start[0]][start[1]] = True
    area = 0
    perimeter = 0
    value = garden[start[0]][start[1]]

    while queue:
        ci, cj = queue.pop()
        area += 1
        for di, dj in directions:
            ni, nj = ci + di, cj + dj
            if 0 <= ni < height and 0 <= nj < width:
                if garden[ni][nj] == value and not visited[ni][nj]:
                    visited[ni][nj] = True
                    queue.append((ni, nj))
                elif garden[ni][nj] != value:  # Different region
                    perimeter += 1
            else:  # Out of bounds
                perimeter += 1
    return area, perimeter


def solve_region_perimeter(
    start: Tuple[int, int],
    garden: List[List[str]],
    directions: List[Tuple[int, int]],
    visited: List[List[bool]],
) -> Tuple[List[Tuple[int, int]], Set[Tuple[int, int, int, int]]]:
    height, width = len(garden), len(garden[0])
    i, j = start
    value = garden[i][j]
    queue = [start]
    perimeter = set()
    vis = set()

    for i, j in queue:
        vis.add((i, j))
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if (
                0 <= ni < height
                and 0 <= nj < width
                and garden[ni][nj] == value
                and (ni, nj) not in vis
            ):
                visited[ni][nj] = True
                vis.add((ni, nj))
                queue.append((ni, nj))
            else:
                if (ni, nj) in vis:
                    continue
                perimeter.add((ni, nj, di, dj))

    return queue, perimeter


def count_fences(perimeters, directions) -> int:
    vis = set()
    nb_fences = 0

    for perimeter in perimeters:
        if perimeter in vis:
            continue
        nb_fences += 1
        r, c, ddr, ddc = perimeter
        queue = [(r, c)]
        vis.add((r, c, ddr, ddc))
        for r, c in queue:
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if (nr, nc, ddr, ddc) in perimeters and (nr, nc, ddr, ddc) not in vis:
                    queue.append((nr, nc))
                    vis.add((nr, nc, ddr, ddc))
    return nb_fences


def compute_sum_area_times_perimeter(garden: List[List[str]]) -> int:
    height, width = len(garden), len(garden[0])
    visited = [[False] * width for _ in range(height)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right

    total_sum = 0
    for i in range(height):
        for j in range(width):
            if not visited[i][j]:
                area, perimeter = flood_fill((i, j), garden, directions, visited)
                total_sum += area * perimeter
    return total_sum


def compute_sum_area_times_fence_perimeter(garden: List[List[str]]) -> int:
    """
    Computes the sum of area times the number of distinct fences (based on perimeter) for all regions.
    """
    height, width = len(garden), len(garden[0])
    visited = [[False] * width for _ in range(height)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    total_sum = 0
    for i in range(height):
        for j in range(width):
            if not visited[i][j]:
                regions, perimeters = solve_region_perimeter(
                    (i, j), garden, directions, visited
                )
                fences = count_fences(perimeters, directions)
                total_sum += len(regions) * fences

    return total_sum


if __name__ == "__main__":
    garden = get_garden_from_input_file("./input.txt")

    # Compute the total price based on area * perimeter
    total_price_perimeter = compute_sum_area_times_perimeter(garden)
    print(
        f"The total price of fencing all regions (area * perimeter) is {total_price_perimeter}"
    )

    # Compute the total price based on area * number of fences
    total_price_fences = compute_sum_area_times_fence_perimeter(garden)
    print(
        f"The total price of fencing all regions (area * fences) is {total_price_fences}"
    )
