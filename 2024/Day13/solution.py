from dataclasses import dataclass
import re
from typing import List, Tuple, Optional


@dataclass
class Button:
    dx: int
    dy: int
    cost: int


@dataclass
class ClawMachine:
    prize: Tuple[int, int]
    buttonA: Button
    buttonB: Button


def get_claw_machines_input_file(file_path: str) -> List[ClawMachine]:
    pattern_button = re.compile(r"X\+(\d+).*Y\+(\d+)")
    pattern_price = re.compile(r"X=(\d+).*Y=(\d+)")
    costA = 3
    costB = 1
    with open(file_path, "r") as file:
        claw_machines = []
        for claw_machine in file.read().strip().split("\n\n"):
            button_a, button_b, prize = claw_machine.strip().split("\n")
            bax, bay = [int(x) for x in pattern_button.findall(button_a)[0]]
            bbx, bby = [int(x) for x in pattern_button.findall(button_b)[0]]
            px, py = [int(x) for x in pattern_price.findall(prize)[0]]
            claw_machines.append(
                ClawMachine(
                    prize=(px, py),
                    buttonA=Button(bax, bay, costA),
                    buttonB=Button(bbx, bby, costB),
                )
            )
        return claw_machines


def solve_claw_machine(
    claw_machine: ClawMachine, shift: int, bounds: Tuple[Optional[int], Optional[int]]
) -> Optional[int]:
    """
    This is a bounded integer linear programming problem.

    System of equations:
        nA * dxA + nB * dxB = px
        nA * dyA + nB * dyB = py

    As a matrix:
        A * n = B       where A = | dxA dxB | , n = | nA | , B = | px |
                                  | dyA dyB |       | nB |       | py |

    Objective function:
        Cost = nA * costA + nB * costB

    Constraints:
        nA and nB are integers and 0 <= nA <= 100 and 0 <= nB <= 100
    """
    px = claw_machine.prize[0] + shift
    py = claw_machine.prize[1] + shift
    dxA = claw_machine.buttonA.dx
    dyA = claw_machine.buttonA.dy
    dxB = claw_machine.buttonB.dx
    dyB = claw_machine.buttonB.dy

    nA = (py * dxB - px * dyB) / (dyA * dxB - dxA * dyB)
    nB = -((py * dxA - px * dyA) / (dyA * dxB - dxA * dyB))

    if (bounds[0] is not None and (bounds[0] > nA or bounds[0] > nB)) or (
        bounds[1] is not None and (bounds[1] < nA or bounds[1] < nB)
    ):
        # Out of bounds
        return None

    if not nA.is_integer() or not nB.is_integer():
        return None

    tokens = int(nA * claw_machine.buttonA.cost + nB * claw_machine.buttonB.cost)
    return tokens


def get_least_tokens_max_prizes(
    claw_machines: List[ClawMachine],
    shift: int,
    bounds: Tuple[Optional[int], Optional[int]],
) -> int:
    total_cost = 0
    for claw_machine in claw_machines:
        cost = solve_claw_machine(claw_machine, shift, bounds)
        if cost:
            total_cost += int(cost)
    return total_cost


if __name__ == "__main__":
    claw_machines = get_claw_machines_input_file("./input.txt")

    # Correct prizes position and bounded to (0, 100)
    tokens = get_least_tokens_max_prizes(claw_machines, shift=0, bounds=(0, 100))
    print(f"the fewest tokens to spend to win all possible prizes is {tokens}")

    # Prizes position shifted and no more upper bound
    tokens = get_least_tokens_max_prizes(
        claw_machines, shift=10000000000000, bounds=(0, None)
    )
    print(f"the fewest tokens to spend to win all possible prizes is {tokens}")
