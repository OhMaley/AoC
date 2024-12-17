from dataclasses import dataclass, field
from re import compile
from typing import Callable, Dict, List, Tuple
from time import sleep


@dataclass
class Alu:
    registers: Dict[str, int] = field(default_factory=lambda: {"A": 0, "B": 0, "C": 0})
    instructions: List[int] = field(default_factory=list)
    instructions_pointer: int = 0
    operations: List[Callable[[], None]] = field(init=False)
    output: List[int] = field(default_factory=list)

    def __post_init__(self):
        self.operations = [
            self.adv,
            self.bxl,
            self.bst,
            self.jnz,
            self.bxc,
            self.out,
            self.bdv,
            self.cdv,
        ]

    def get_value_from_combo(self, combo: int) -> int:
        return [0, 1, 2, 3, registers["A"], registers["B"], registers["C"]][combo]

    def adv(self) -> None:
        self.registers["A"] = self.registers["A"] // 2 ** self.get_value_from_combo(
            self.instructions[self.instructions_pointer + 1]
        )
        self.instructions_pointer += 2

    def bxl(self) -> None:
        self.registers["B"] = (
            self.registers["B"] ^ self.instructions[self.instructions_pointer + 1]
        )
        self.instructions_pointer += 2

    def bst(self) -> None:
        self.registers["B"] = (
            self.get_value_from_combo(self.instructions[self.instructions_pointer + 1])
            % 8
        )
        self.instructions_pointer += 2

    def jnz(self) -> None:
        if self.registers["A"] == 0:
            self.instructions_pointer += 2
        else:
            self.instructions_pointer = self.instructions[self.instructions_pointer + 1]

    def bxc(self) -> None:
        self.registers["B"] = self.registers["B"] ^ self.registers["C"]
        self.instructions_pointer += 2

    def out(self) -> None:
        result: int = (
            self.get_value_from_combo(self.instructions[self.instructions_pointer + 1])
            % 8
        )
        self.output.append(result)
        self.instructions_pointer += 2

    def bdv(self) -> None:
        self.registers["B"] = self.registers["A"] // 2 ** self.get_value_from_combo(
            self.instructions[self.instructions_pointer + 1]
        )
        self.instructions_pointer += 2

    def cdv(self) -> None:
        self.registers["C"] = self.registers["A"] // 2 ** self.get_value_from_combo(
            self.instructions[self.instructions_pointer + 1]
        )
        self.instructions_pointer += 2

    def print_output(self) -> None:
        print(",".join([str(x) for x in self.output]))

    def reset(self):
        self.registers["A"] = 0
        self.registers["B"] = 0
        self.registers["C"] = 0
        self.instructions_pointer = 0
        self.output = []

    def run_program(self) -> None:
        while self.instructions_pointer < len(self.instructions):
            self.operations[self.instructions[self.instructions_pointer]]()

    def debug_program(self, pointer, registry_a) -> bool:
        if pointer < 0:
            return True

        for d in range(8):
            a, i = registry_a << 3 | d, 0

            self.reset()
            self.registers["A"] = a
            self.instructions_pointer = i

            while self.instructions_pointer < len(self.instructions):
                self.operations[self.instructions[self.instructions_pointer]]()
                if len(self.output) > 0:
                    break

            if self.output[-1] == self.instructions[pointer] and self.debug_program(
                pointer - 1, registry_a << 3 | d
            ):
                return True
        return False


def find_perfect_value(alu: Alu) -> int:
    alu.debug_program(len(alu.instructions) - 1, 0)
    return alu.registers["A"]


def get_registers_and_program_from_input_file(
    file_path: str,
) -> Tuple[Dict[str, int], List[int]]:
    with open(file_path, "r") as file:
        registers_str, program_str = file.read().strip().split("\n\n")

        # Registers
        pattern = compile(r"(\w*)\s*:\s*(\d*)")
        registers = {k: int(v) for k, v in pattern.findall(registers_str.strip())}

        # Program
        program = program_str.strip().split(":")[1].strip().split(",")
        program = [int(x) for x in program]
        return registers, program


if __name__ == "__main__":
    registers, program = get_registers_and_program_from_input_file("./input.txt")
    alu = Alu(registers=registers, instructions=program)

    # Get output of the given program
    alu.run_program()
    alu.print_output()

    # Get the lowest value of register A so the program outputs its program
    lowest_perfect_register_a = find_perfect_value(alu)
    print(f"The perfect value of register A is {lowest_perfect_register_a}")
