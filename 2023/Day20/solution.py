from __future__ import annotations
from typing import List, Dict, Union
from abc import ABC, abstractmethod
from collections import deque


class Module(ABC):
    def __init__(
        self,
        name: str,
        module_type: str,
        inputs: List[Module] | None = None,
        outputs: List[Module] | None = None,
    ) -> None:
        self.name = name
        self.module_type = module_type
        self.inputs = inputs if inputs else []
        self.outputs = outputs if outputs else []
        self.input_signals = [-1 for _ in range(len(self.inputs))]
        self.output_signals = [-1 for _ in range(len(self.outputs))]
        self.pulse_counter = [0, 0]

    def add_inputs(self, inputs: List[Module]) -> None:
        for module in inputs:
            if module not in self.inputs:
                self.inputs.append(module)
                self.input_signals.append(-1)

    def add_outputs(self, outputs: List[Module]) -> None:
        for module in outputs:
            if module not in self.outputs:
                self.outputs.append(module)
                self.output_signals.append(-1)

    @abstractmethod
    def apply(self) -> List[Module]:
        pass

    def __repr__(self) -> str:
        s = ", ".join(m.name for m in self.inputs)
        type_to_symbol = {
            "flip-flop": "%",
            "conjunction": "&",
            "button": "",
            "broadcaster": "",
            "": "",
        }
        s += f" -> {type_to_symbol[self.module_type]}{self.name} -> "
        s += ", ".join(m.name for m in self.outputs)
        return s


class FlipFlop(Module):
    def __init__(
        self,
        name: str,
        inputs: List[Module] = [],
        outputs: List[Module] = [],
    ) -> None:
        super().__init__(name, "flip-flop", inputs, outputs)
        self.on = False
        self.init_on = self.on

    def apply(self) -> List[Module]:
        if any([pulse == 0 for pulse in self.input_signals]):
            self.on = not self.on
            self.output_signals = [1 if self.on else 0 for _ in self.outputs]
            self.pulse_counter[1 if self.on else 0] += len(self.outputs)
            self.input_signals = [-1 for _ in self.input_signals]
            return self.outputs
        self.input_signals = [-1 for _ in self.input_signals]
        return []


class Conjunction(Module):
    def __init__(
        self, name: str, inputs: List[Module] = [], outputs: List[Module] = []
    ) -> None:
        super().__init__(name, "conjunction", inputs, outputs)
        self.last_input_pulses = [0 for _ in self.inputs]
        self.init_last_input_pulses = [x for x in self.last_input_pulses]

    def add_inputs(self, inputs: List[Module]) -> None:
        super().add_inputs(inputs)
        self.last_input_pulses = [0 for _ in self.inputs]
        self.init_last_input_pulses = [x for x in self.last_input_pulses]

    def apply(self) -> List[Module]:
        self.last_input_pulses = [
            v if v != -1 else self.last_input_pulses[i]
            for i, v in enumerate(self.input_signals)
        ]
        self.output_signals = [
            0 if all(self.last_input_pulses) else 1 for _ in self.outputs
        ]
        self.pulse_counter[0 if all(self.last_input_pulses) else 1] += len(self.outputs)
        self.input_signals = [-1 for _ in self.input_signals]
        return self.outputs


class Broadcaster(Module):
    def __init__(
        self,
        name: str,
        inputs: List[Module] = [],
        outputs: List[Module] = [],
    ) -> None:
        super().__init__(name, "broadcaster", inputs, outputs)

    def apply(self) -> List[Module]:
        val = 1 if any(self.input_signals) else 0
        self.output_signals = [val for v in self.outputs]
        for i in [0, 1]:
            self.pulse_counter[i] += len([i for x in self.output_signals if x == i])
        self.input_signals = [-1 for _ in self.input_signals]
        return self.outputs


class Button(Module):
    def __init__(
        self,
        name: str,
        outputs: List[Module] = [],
    ) -> None:
        super().__init__(name, "button", [], outputs)

    def apply(self) -> List[Module]:
        self.output_signals = [0 for _ in self.outputs]
        self.pulse_counter[0] += len(self.outputs)
        self.input_signals = [-1 for _ in self.input_signals]
        return self.outputs


class Other(Module):
    def __init__(
        self,
        name: str,
        inputs: List[Module] | None = None,
    ) -> None:
        super().__init__(name, "", inputs, [])

    def apply(self) -> List[Module]:
        return []


config_map: Dict[str, Dict[str, Union[str, List[str]]]] = {}
with open("input.txt", "r") as file:
    for module_config in file.read().strip().split("\n"):
        print(module_config)
        type_and_name, outputs = module_config.split("->")

        module_type = ""
        module_name = ""
        if "broadcaster" in type_and_name:
            module_type = "broadcaster"
            module_name = "broadcaster"
        elif "%" in type_and_name:
            module_type = "flip-flop"
            module_name = type_and_name.strip()[1:]
        elif "&" in type_and_name:
            module_type = "conjunction"
            module_name = type_and_name.strip()[1:]
        else:
            print(f"ERROR: cannot extract type from {type_and_name}")
            exit()

        output_list = [x.strip() for x in outputs.strip().split(",")]

        module = config_map.setdefault(module_name, {})
        module.setdefault("type", module_type)
        outputs = module.setdefault("outputs", output_list)
        inputs = module.setdefault("inputs", [])
        for input_module_name in output_list:
            input_module_name = config_map.setdefault(input_module_name, {})
            input_module_inputs = input_module_name.setdefault("inputs", [])
            if module_name not in input_module_inputs:
                input_module_inputs.append(module_name)  # type: ignore

# Add the Button
config_map["button"] = {"type": "button", "outputs": ["broadcaster"], "inputs": []}
config_map["broadcaster"]["inputs"].append("button")  # type: ignore

# Instanciate the classes
modules: Dict[str, Module] = {}
for module_name, config in config_map.items():
    if "type" in config:
        if config["type"] == "button":
            modules[module_name] = Button(module_name)
        elif config["type"] == "broadcaster":
            modules[module_name] = Broadcaster(module_name)
        elif config["type"] == "flip-flop":
            modules[module_name] = FlipFlop(module_name)
        elif config["type"] == "conjunction":
            modules[module_name] = Conjunction(module_name)
    else:
        modules[module_name] = Other(module_name)


for module_name, config in config_map.items():
    if "inputs" in config:
        modules[module_name].add_inputs([modules[x] for x in config["inputs"]])
    if "outputs" in config:
        modules[module_name].add_outputs([modules[x] for x in config["outputs"]])


def run_one_cycle():
    start_module = modules["button"]
    queue: deque[Module] = deque()
    queue.append(start_module)

    while queue:
        current_modules: List[Module] = []
        next_modules: List[Module] = []
        while queue:
            module = queue.popleft()
            current_modules.append(module)
            next_receivers = module.apply()
            next_modules += next_receivers
        for module in current_modules:
            for output_module in module.outputs:
                input_index = next(
                    (
                        i
                        for i, m in enumerate(module.outputs)
                        if m.name == output_module.name
                    ),
                    0,
                )
                output_index = next(
                    (
                        i
                        for i, m in enumerate(output_module.inputs)
                        if m.name == module.name
                    ),
                    0,
                )
                output_module.input_signals[output_index] = module.output_signals[
                    input_index
                ]
        queue.extend(next_modules)


print("---------------------------")
for _ in range(1000):
    run_one_cycle()

total = [0, 0]
for module in modules.values():
    total = [a + b for a, b in zip(total, module.pulse_counter)]

print(total, total[0] * total[1])
