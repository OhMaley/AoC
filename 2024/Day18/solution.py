from collections import deque
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Memory:
    width: int
    height: int
    corrupted_memory: List[Tuple[int, int]]

    def __str__(self) -> str:
        s = f"Memory space of size {self.width} x {self.height}"
        s += "\n" + "\n".join(
            ["".join("." for j in range(self.width)) for i in range(self.height)]
        )
        return s

    def display_path(self, at_step: int, path: List[Tuple[int, int]]) -> None:
        display_grid = [["." for x in range(self.width)] for y in range(self.height)]
        for corrupted in self.corrupted_memory[:at_step]:
            x, y = corrupted
            display_grid[y][x] = "#"
        for coord in path:
            x, y = coord
            display_grid[y][x] = "O"
        s = "\n".join(["".join(c for c in line) for line in display_grid])
        print(s)

    def find_best_path(
        self, start: Tuple[int, int], end: Tuple[int, int], at_step: int
    ) -> List[Tuple[int, int]]:
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        queue = deque([(start, [start])])  # Stores (current position, path so far)
        visited = set()  # Set to keep track of visited nodes
        visited.add(start)

        while queue:
            # Dequeue the next node to explore
            current, path = queue.popleft()

            # If we reach the goal, return the path
            if current == end:
                return path

            # Explore neighbors
            for dx, dy in directions:
                neighbor = (current[0] + dx, current[1] + dy)

                # Check if the neighbor is within bounds and is not a corrupted memory
                if (
                    0 <= neighbor[0] < self.width
                    and 0 <= neighbor[1] < self.height
                    and neighbor not in self.corrupted_memory[: at_step + 1]
                    and neighbor not in visited
                ):
                    # Mark neighbor as visited and add to queue
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return []

    def find_first_dump(
        self, start: Tuple[int, int], end: Tuple[int, int], min_step: int, max_step: int
    ) -> Tuple[int, int]:
        step = min_step
        best_path = self.find_best_path(start, end, step)
        while step < max_step and len(best_path) > 0:
            step += 1
            if self.corrupted_memory[step] in best_path:
                best_path = self.find_best_path(start, end, step)
        return self.corrupted_memory[step]


def get_bytes_position_from_input_file(file_path: str) -> List[Tuple[int, int]]:
    with open(file_path, "r") as file:
        bytes_position = []
        for line in file.read().strip().split("\n"):
            x, y = line.split(",")
            bytes_position.append((int(x), int(y)))
        return bytes_position


if __name__ == "__main__":
    bytes_position = get_bytes_position_from_input_file("./input.txt")
    width = 71
    height = 71
    memory = Memory(width, height, bytes_position)

    # Find best path
    start = (0, 0)
    end = (width - 1, height - 1)
    at_step = 1024
    best_path = memory.find_best_path(start, end, at_step)
    print(f"The minimum number of steps to reach the exit is {len(best_path) - 1}")

    # Find the first corrupted memory that would close the path
    first_dump_position = memory.find_first_dump(
        start, end, at_step, len(memory.corrupted_memory) - 1
    )
    print(
        f"the coordinates of the first byte that will prevent the exit from being reachable from your starting position is {first_dump_position}"
    )
