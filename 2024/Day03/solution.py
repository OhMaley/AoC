from typing import List, Pattern, Tuple
from math import prod
import re


def get_corrupted_memory_from_input_file(file_path: str) -> str:
    with open(file_path, "r") as file:
        return "".join(file.read().strip().split("\n"))


def find_mul_instructions(memory: str) -> List[List[int]]:
    # Regex to find the mutiplication pattern an match the 2 numbers
    prog: Pattern[str] = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    return [[int(x) for x in match] for match in prog.findall(memory)]


def find_enabled_mul_instructions(memory: str) -> List[List[int]]:
    # Remove the part of the string between "don't()" and "do()" of the end of the string
    prog: Pattern[str] = re.compile(r"don't\(\).*?(?:do\(\)|$)")
    enabled_memory_parts: str = prog.sub("", memory)
    return find_mul_instructions(enabled_memory_parts)


def compute_mul(instructions: List[List[int]]) -> int:
    return sum(prod(instruction) for instruction in instructions)


if __name__ == "__main__":
    corrupted_memory: str = get_corrupted_memory_from_input_file("./input.txt")

    instructions: List[List[int]] = find_mul_instructions(corrupted_memory)
    result: int = compute_mul(instructions)
    print(f"Sum of all multiplications = {result}")

    instructions: List[List[int]] = find_enabled_mul_instructions(corrupted_memory)
    result: int = compute_mul(instructions)
    print(f"Sum of all enabled multiplications = {result}")
