from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
import heapq
from itertools import chain
from typing import List, Tuple


class Direction(Enum):
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)


@dataclass
class Maze:
    height: int
    width: int
    grid: List[List[str]]
    start: Tuple[int, int]
    end: Tuple[int, int]

    @classmethod
    def create_from_string(cls, s: str):
        lines = s.split("\n")
        height = len(lines)
        width = len(lines[0])
        grid = [list(line) for line in lines]

        # Extract the start position
        start = next(
            (r, c)
            for r, row in enumerate(grid)
            for c, char in enumerate(row)
            if char == "S"
        )

        # Extract the end position
        end = next(
            (r, c)
            for r, row in enumerate(grid)
            for c, char in enumerate(row)
            if char == "E"
        )

        # Only keep walls and empty space in the grid
        grid = [[char if char in ("#", ".") else "." for char in row] for row in grid]

        return cls(height, width, grid, start, end)

    def __str__(self) -> str:
        display_grid = [row[:] for row in self.grid]

        # Place the start
        r, c = self.start
        display_grid[r][c] = "S"

        # Place the end
        r, c = self.end
        display_grid[r][c] = "E"

        # Concat all info
        s = f"Maze of size {self.width} x {self.height}"
        s += "\n" + "\n".join(["".join(c for c in line) for line in display_grid])
        return s

    def display_path(self, path: List[Tuple[int, int]]) -> None:
        display_grid = [row[:] for row in self.grid]
        for coord in path:
            r, c = coord
            display_grid[r][c] = "O"
        s = "\n" + "\n".join(["".join(c for c in line) for line in display_grid])
        print(s)

    def find_best_path(
        self, start_direction: Direction, forward_cost: int, rotation_cost: int
    ) -> Tuple[int, List[Tuple[int, int]]]:
        # Dijkstra
        visited = set()
        min_heap = [
            (0, self.start, start_direction.value, [])
        ]  # (current_cost, current_position, current_direction, path_taken)

        while min_heap:
            current_cost, current_pos, current_dir, path = heapq.heappop(min_heap)

            if current_pos in visited:
                continue

            visited.add(current_pos)

            # Update the path
            path = path + [current_pos]

            # Check if we've reached the end
            if current_pos == self.end:
                return current_cost, path

            # Explore neighbors
            x, y = current_pos
            for dir in Direction:
                dx, dy = dir.value
                nx, ny = x + dx, y + dy

                # Check that the neighbor is not a wall and that it has not been already visited
                if self.grid[nx][ny] != "#" and (nx, ny) not in visited:
                    # Compute the cost
                    step_cost = (
                        rotation_cost
                        * max(abs(a - b) for a, b in zip(current_dir, dir.value))
                        + forward_cost
                    )
                    heapq.heappush(
                        min_heap, (current_cost + step_cost, (nx, ny), dir.value, path)
                    )

        return -1, []  # No path found

    def find_all_best_paths(
        self, start_direction: Direction, forward_cost: int, rotation_cost: int
    ) -> Tuple[int, List[List[Tuple[int, int]]]]:
        min_heap = [
            (0, self.start, start_direction.name, [self.start])
        ]  # (current_cost, current_position, current_direction, path_taken)
        min_cost = defaultdict(lambda: 1000000000)
        min_cost[(self.start, start_direction.name)] = 0
        best_paths_dict = defaultdict(list)

        while min_heap:
            current_cost, current_pos, current_dir, path = heapq.heappop(min_heap)

            if current_cost > min_cost[(current_pos, current_dir)]:
                continue

            if current_pos == self.end:
                if not best_paths or current_cost == min(
                    min_cost[(self.end, d)] for d in [d.name for d in Direction]
                ):
                    best_paths_dict[current_cost].append(path)
                continue

            # Explore neighbors
            x, y = current_pos
            for direction in Direction:
                new_dir = direction.name
                dx, dy = direction.value
                nx, ny = x + dx, y + dy

                # Check that the neighbor is not a wall
                if self.grid[nx][ny] != "#":
                    # Compute the cost
                    step_cost = (
                        rotation_cost
                        * max(
                            abs(a - b)
                            for a, b in zip(
                                getattr(Direction, current_dir).value, (dx, dy)
                            )
                        )
                        + forward_cost
                    )
                    new_cost = current_cost + step_cost
                    if new_cost < min_cost[((nx, ny), new_dir)]:
                        min_cost[((nx, ny), new_dir)] = new_cost
                        heapq.heappush(
                            min_heap, (new_cost, (nx, ny), new_dir, path + [(nx, ny)])
                        )
                    elif new_cost == min_cost[((nx, ny), new_dir)]:
                        heapq.heappush(
                            min_heap, (new_cost, (nx, ny), new_dir, path + [(nx, ny)])
                        )

        min_cost_to_end = min(best_paths_dict.keys())
        return min_cost_to_end, best_paths_dict[min_cost_to_end]


def get_maze_from_input_file(file_path: str) -> Maze:
    with open(file_path, "r") as file:
        return Maze.create_from_string(file.read().strip())


if __name__ == "__main__":
    maze = get_maze_from_input_file("./input.txt")

    # Minimum cost of the best path
    cost, best_paths = maze.find_best_path(
        start_direction=Direction.EAST, forward_cost=1, rotation_cost=1000
    )
    print(f"The lowest score a Reindeer could possibly get is {cost}")

    # Number of unique tiles in all best paths union
    cost, best_paths = maze.find_all_best_paths(
        start_direction=Direction.EAST, forward_cost=1, rotation_cost=1000
    )
    unique_tiles = set(chain(*best_paths))
    print(
        f"There are {len(unique_tiles)} tiles that are at least on one of the best paths"
    )
