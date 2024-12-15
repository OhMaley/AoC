from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Warehouse:
    width: int
    height: int
    grid: List[List[str]]
    robot: Tuple[int, int]
    boxes: List[List[Tuple[int, int]]]
    wider: bool
    box_char: str

    @classmethod
    def create_from_string(cls, s: str, wider: bool = False):
        lines = s.strip().split("\n")
        grid = [list(line) for line in lines]
        width = len(lines[0])
        height = len(lines)
        box_char = "O"

        # Transform the warehouse is case of a wide warehouse
        if wider:
            char_map = {"#": "##", "O": "[]", ".": "..", "@": "@."}
            box_char = "[]"
            grid = []
            for line in lines:
                transformed_line = "".join(char_map[char] for char in line)
                grid.append(transformed_line)
            width = len(grid[0])

        # Extract robot position
        robot = next(
            (r, c)
            for r, row in enumerate(grid)
            for c, char in enumerate(row)
            if char == "@"
        )

        # Extract all boxes positions
        boxes = []
        for r, row in enumerate(grid):
            for c, char in enumerate(row):
                if char == box_char[0]:
                    coord = []
                    for i in range(len(box_char)):
                        coord.append((r, c + i))
                    boxes.append(coord)

        # Remove the boxes and the robot from the grid, only keep the walls
        grid = [
            [char if char not in ("O", "@", "[", "]") else "." for char in row]
            for row in grid
        ]

        return cls(width, height, grid, robot, boxes, wider, box_char)

    def __str__(self) -> str:
        display_grid = [row[:] for row in self.grid]

        # Place the robot
        r, c = self.robot
        display_grid[r][c] = "@"

        # Place the boxes
        for box in self.boxes:
            for i, coord in enumerate(box):
                r, c = coord
                display_grid[r][c] = self.box_char[i]

        # Concat all info
        s = f"Warehouse of size {self.width} x {self.height}"
        s += "\n" + f"Robot in {self.robot}"
        s += "\n" + "\n".join(["".join(c for c in line) for line in display_grid])
        return s

    def get_sum_boxes_GPS(self) -> int:
        return sum([100 * box[0][0] + box[0][1] for box in self.boxes])

    def simulate_sequence(self, sequence: str) -> None:
        for c in sequence:
            self.simulate(c)

    def simulate(self, direction: str):
        directions = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}

        # Get the next robot position
        dr, dc = directions[direction]
        r, c = self.robot
        next_r, next_c = r + dr, c + dc

        # If wall --> do nothing
        if self.grid[next_r][next_c] == "#":
            return

        # If box
        boxes_flatten = [coord for box in self.boxes for coord in box]
        if (next_r, next_c) in boxes_flatten:
            # Find all consecutive boxes in the direction of the push
            chain_to_push = self.get_chain_of_box(direction)

            # Check the chain of boxes can move
            can_move = self.check_chain_boxes_can_move(chain_to_push, direction)
            if not can_move:
                # Bocked by a wall --> do nothing
                return

            # Move all boxes
            for box in reversed(chain_to_push):
                self.boxes.remove(box)
                self.boxes.append([(coord[0] + dr, coord[1] + dc) for coord in box])

        # Move the robot
        self.robot = (next_r, next_c)

    def get_chain_of_box(self, direction: str) -> List[List[Tuple[int, int]]]:
        chain_to_push = []
        directions = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}
        dr, dc = directions[direction]
        r, c = self.robot
        next_r, next_c = r + dr, c + dc
        boxes_flatten = [coord for box in self.boxes for coord in box]
        first_box = next(box for box in self.boxes if (next_r, next_c) in box)
        visited = []
        queue = [first_box]
        while queue:
            box = queue.pop()
            if box in visited:
                continue
            visited.append(box)
            chain_to_push.append(box)

            # Check neighbors in the direction of the movement
            for coord in box:
                coord_r, coord_c = coord
                neighbor_r, neighbor_c = coord_r + dr, coord_c + dc
                if (neighbor_r, neighbor_c) in boxes_flatten:
                    neighbor_box = next(
                        box for box in self.boxes if (neighbor_r, neighbor_c) in box
                    )
                    queue.append(neighbor_box)

        return chain_to_push

    def check_chain_boxes_can_move(
        self, chain_of_boxes: List[List[Tuple[int, int]]], direction: str
    ) -> bool:
        directions = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}
        dr, dc = directions[direction]

        # For all boxes check what is behind
        cells_behind_boxes = []
        for box in chain_of_boxes:
            for coord in box:
                cell_behind = (coord[0] + dr, coord[1] + dc)
                cells_behind_boxes.append(cell_behind)

        if any([self.grid[cell[0]][cell[1]] == "#" for cell in cells_behind_boxes]):
            return False

        return True


def get_map_and_movements_from_input_file(
    file_path: str, wider: bool = False
) -> Tuple[Warehouse, str]:
    with open(file_path, "r") as file:
        warehouse, movements = file.read().strip().split("\n\n")
        return Warehouse.create_from_string(warehouse, wider), "".join(
            line for line in movements.split("\n")
        )


if __name__ == "__main__":
    # Classic warehouse map with 1 cell wide boxes
    warehouse, movements = get_map_and_movements_from_input_file("./input.txt")
    warehouse.simulate_sequence(movements)
    print(f"The sum of all boxes' GPS coordinates is {warehouse.get_sum_boxes_GPS()}")

    # Wider warehouse with 2 cells wide boxes
    warehouse, movements = get_map_and_movements_from_input_file(
        "./input.txt", wider=True
    )
    warehouse.simulate_sequence(movements)
    print(f"The sum of all boxes' GPS coordinates is {warehouse.get_sum_boxes_GPS()}")
