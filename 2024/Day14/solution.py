import math
import re
import time
import threading
from typing import List, Tuple


lock = threading.Lock()


def get_robots_input_file(file_path: str) -> List[Tuple[int, int, int, int]]:
    pattern = re.compile(r"p=(\d+),(\d+)\s+v=(-?\d+),(-?\d+)")
    robots = []
    with open(file_path, "r") as file:
        for robot in file.read().strip().split("\n"):
            px, py, vx, vy = [int(x) for x in pattern.findall(robot)[0]]
            robots.append((px, py, vx, vy))
    return robots


def simulate(
    robots: List[Tuple[int, int, int, int]], delta_time: int, height: int, width: int
) -> List[Tuple[int, int]]:
    future_robots_position = []
    for robot in robots:
        px, py, vx, vy = robot
        future_px = (px + delta_time * vx) % width
        future_py = (py + delta_time * vy) % height
        future_robots_position.append((future_px, future_py))
    return future_robots_position


def get_safety_factor(
    robots_position: List[Tuple[int, int]], height: int, width: int
) -> int:
    robots_per_quadrants = [0, 0, 0, 0]
    mid_width = width // 2
    mid_height = height // 2
    for position in robots_position:
        if position[0] < mid_width and position[1] < mid_height:
            # Top left
            robots_per_quadrants[0] += 1
        elif position[0] > mid_width and position[1] < mid_height:
            # Top right
            robots_per_quadrants[1] += 1
        elif position[0] < mid_width and position[1] > mid_height:
            # Bottom left
            robots_per_quadrants[2] += 1
        elif position[0] > mid_width and position[1] > mid_height:
            # Bottom right
            robots_per_quadrants[3] += 1

    return math.prod(robots_per_quadrants)


def pretty_print(
    future_positions: List[Tuple[int, int]], height: int, width: int
) -> None:
    s = ""
    for i in range(width):
        for j in range(height):
            if (i, j) in future_positions:
                s += "#"
            else:
                s += "."
        s += "\n"
    s += "\n"
    print(s)


def simulate_and_print(robots, height, width):
    t = 179
    while True:
        with lock:
            future_positions = simulate(robots, t, height, width)
            print(f"t> = {t}")
            pretty_print(future_positions, height, width)
            t += 103
        time.sleep(0.5)


if __name__ == "__main__":
    robots = get_robots_input_file("./input.txt")
    width = 101
    height = 103

    # Simulate 100s
    future_robots_position = simulate(robots, 100, height, width)
    safety_factor = get_safety_factor(future_robots_position, height, width)
    print(safety_factor)

    # Simulate frame by frame
    # Vertical pattern is forming (for me) every 103s starting at the 76s
    # So play with it until you visually find the pattern
    message_thread = threading.Thread(
        target=simulate_and_print, args=(robots, height, width), daemon=True
    )
    message_thread.start()

    while True:
        time.sleep(0.5)
