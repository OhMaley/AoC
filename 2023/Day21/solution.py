from typing import List, Tuple, Dict
from collections import deque


DIRECTIONS = [(-1, 0), (0, -1), (1, 0), (0, 1)]

garden: List[str] = []
with open("input.txt", "r") as file:
    garden = file.read().strip().split("\n")

# print("---------------")
# for line in garden:
#     print(line)
# print("---------------")


def bfs(start: Tuple[int, int], max_depth: int, graph: List[str]) -> List[List[int]]:
    height = len(graph)
    width = len(graph[0])
    visited = [[False for j in range(width)] for i in range(height)]
    visited[start[0]][start[1]] = True
    queue = deque([start])
    dist = [[-1 for j in range(width)] for i in range(height)]
    dist[start[0]][start[1]] = 0

    while queue:
        current = queue.popleft()
        neighbors = [
            (current[0] + dx, current[1] + dy)
            for dx, dy in DIRECTIONS
            if 0 <= current[0] + dx < height
            and 0 <= current[1] + dy < width
            and graph[current[0] + dx][current[1] + dy] != "#"
        ]
        for neighbor in neighbors:
            if not visited[neighbor[0]][neighbor[1]]:
                visited[neighbor[0]][neighbor[1]] = True
                dist[neighbor[0]][neighbor[1]] = dist[current[0]][current[1]] + 1
                if dist[neighbor[0]][neighbor[1]] < max_depth:
                    queue.append(neighbor)

    return dist


height = len(garden)
width = len(garden[0])
nb_steps = 26501365
distances: Dict[Tuple, List[List[int]]] = {}

starting_coord = (-1, -1)
for i, line in enumerate(garden):
    for j, c in enumerate(line):
        if c == "S":
            starting_coord = (i, j)
            break
distances[starting_coord] = bfs(starting_coord, nb_steps, garden)


# PART 1
nb_possibilities_p1 = 0
for i, row in enumerate(distances[starting_coord]):
    for j, dist in enumerate(row):
        if dist > -1 and dist <= nb_steps and dist % 2 == nb_steps % 2:
            nb_possibilities_p1 += 1

print(f"Part 1: possibilities={nb_possibilities_p1}")


# PART 2
nb_even_corners = 0
nb_odd_corners = 0
nb_even_full = 0
nb_odd_full = 0
for i, row in enumerate(distances[starting_coord]):
    for j, dist in enumerate(row):
        nb_even_full += 1 if dist % 2 == 0 else 0
        nb_odd_full += 1 if dist % 2 else 0
        if dist > 65:
            nb_even_corners += 1 if dist % 2 == 0 else 0
            nb_odd_corners += 1 if dist % 2 else 0

print(
    f"nb_even_corners={nb_even_corners}, nb_odd_corners={nb_odd_corners}, nb_even_full={nb_even_full}, nb_odd_full={nb_odd_full}"
)

n = 202300
nb_possibilities_p2 = (
    ((n + 1) * (n + 1)) * nb_odd_full
    + (n * n) * nb_even_full
    - (n + 1) * nb_odd_corners
    + n * nb_even_corners
)
# (((n+1)^2)*odd)+((n^2)*even)-((n+1)*ocorn)+(n*ecorn)
print(f"Part 2: possibilities={nb_possibilities_p2}")
