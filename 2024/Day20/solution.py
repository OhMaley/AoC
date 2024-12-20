import networkx
from networkx import Graph
from typing import List, Tuple, Dict


def get_reachable(
    racetrack: List[str], height: int, width: int, node: Tuple[int, int], max_dist: int
) -> List[Tuple[int, int]]:
    reachable: List[Tuple[int, int]] = []
    for dx in range(-max_dist, max_dist + 1):
        remaining_dist = max_dist - abs(dx)
        for dy in range(-remaining_dist, remaining_dist + 1):
            if dx == dy == 0:
                continue
            x, y = node
            nx, ny = x + dx, y + dy
            if 0 <= nx < height and 0 <= ny < width and racetrack[nx][ny] in ".SE":
                reachable.append((nx, ny))
    return reachable


def count_shortest_paths_with_cheats(
    graph: Graph,
    racetrack: List[str],
    height: int,
    width: int,
    normal_path: Dict[Tuple[int, int], int],
    cheat_size: int,
    min_savings: int,
) -> int:
    total = 0
    for node in graph.nodes:
        i, j = node
        reachable = get_reachable(racetrack, height, width, node, cheat_size)
        for dx, dy in reachable:
            cost = abs(i - dx) + abs(j - dy)
            savings = normal_path[(i, j)] - (normal_path[(dx, dy)] + cost)
            if savings >= min_savings:
                total += 1
    return total


def get_racetrack_from_input_file(file_path: str) -> List[str]:
    with open(file_path, "r") as file:
        return file.read().strip().splitlines()


if __name__ == "__main__":
    racetrack = get_racetrack_from_input_file("./input.txt")

    # Testing the networkx library
    graph = Graph()
    start: Tuple[int, int]
    end: Tuple[int, int]
    height = len(racetrack)
    width = len(racetrack[0])

    # Construct the nodes
    for i, line in enumerate(racetrack):
        for j, c in enumerate(line):
            if c in ".SE":
                graph.add_node((i, j))
                if c == "S":
                    start = (i, j)
                if c == "E":
                    end = (i, j)

    # Construct the edges
    for i, line in enumerate(racetrack):
        for j, c in enumerate(line):
            if c in ".SE":
                for dx, dy in [(0, 1), (1, 0)]:
                    nx, ny = i + dx, j + dy
                    if (
                        0 <= nx < height
                        and 0 <= ny < width
                        and racetrack[nx][ny] != "#"
                    ):
                        graph.add_edge((i, j), (nx, ny))

    # compute the normal path
    normal_path: Dict[Tuple[int, int], int] = dict(
        networkx.shortest_path_length(graph, target=end)
    )

    # Find the number of short path with a cheat size of 2
    cheat_size = 2
    min_savings = 100
    total = count_shortest_paths_with_cheats(
        graph, racetrack, height, width, normal_path, cheat_size, min_savings
    )
    print(f"{total} 2-picoseconds cheats would save at least 100 picoseconds")

    # Find the number of short path with a cheat size of 20
    cheat_size = 20
    min_savings = 100
    total = count_shortest_paths_with_cheats(
        graph, racetrack, height, width, normal_path, cheat_size, min_savings
    )
    print(f"{total} 20-picoseconds cheats would save at least 100 picoseconds")
