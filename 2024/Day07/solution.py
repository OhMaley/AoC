from typing import List, Tuple
import operator


def get_calibration_equations_from_input_file(
    file_path: str,
) -> List[Tuple[int, List[int]]]:
    calibration_equations: List[Tuple[int, List[int]]] = []
    with open(file_path, "r") as file:
        equations = file.read().strip().split("\n")

        for equation in equations:
            test_value_str, numbers_str = equation.split(":")

            test_value = int(test_value_str.strip())
            numbers = [int(x) for x in numbers_str.strip().split()]
            calibration_equations.append((test_value, numbers))
    return calibration_equations


def get_total_calibration_results(
    equations: List[Tuple[int, List[int]]], operators: List[str]
) -> int:
    return sum(
        equation[0] for equation in equations if can_be_valid(equation, operators)
    )


def can_be_valid(equation: Tuple[int, List[int]], operators: List[str]) -> bool:
    test_value, numbers = equation
    op_map = {
        "+": operator.add,
        "*": operator.mul,
        "||": lambda x, y: int(str(x) + str(y)),
    }

    def evaluate(value: int, index: int) -> bool:
        if value > test_value:
            return False
        if index == len(numbers):
            return value == test_value
        for op in operators:
            next_value = op_map[op](value, numbers[index])
            if evaluate(next_value, index + 1):
                return True
        return False

    return evaluate(numbers[0], 1)


if __name__ == "__main__":
    calibration_equations = get_calibration_equations_from_input_file("./input.txt")

    # Get the total calibration results with + and *
    operators = ["+", "*"]
    total = get_total_calibration_results(calibration_equations, operators)
    print(f"The total calibration result with + and * is {total}")

    # Get the total calibration results with +, * and ||
    operators = ["+", "*", "||"]
    total = get_total_calibration_results(calibration_equations, operators)
    print(f"The total calibration result with +, * and || is {total}")
