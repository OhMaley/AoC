import graphviz
from sympy import symbols, Eq, solve
from typing import Dict, List, Tuple


def get_initial_values_and_gates_from_input_file(
    file_path: str,
) -> Tuple[Dict[str, int], List[Tuple[str, str, str, str]]]:
    with open(file_path, "r") as file:
        initial_values_str, gates_str = file.read().strip().split("\n\n")

        initial_values = {}
        for line in initial_values_str.strip().split("\n"):
            wire, value = line.split(":")
            initial_values[wire.strip()] = int(value.strip())

        gates = []
        for line in gates_str.strip().split("\n"):
            inputs, output = line.split("->")
            inputs = inputs.strip()
            output = output.strip()

            wire1, gate_type, wire2 = inputs.split()
            gates.append((wire1, gate_type, wire2, output))

        return initial_values, gates


def solve_logic_system(
    initial_values: Dict[str, int], gates: List[Tuple[str, str, str, str]]
) -> Dict[str, int]:
    # Get all wire names
    wire_names = set(initial_values.keys())
    for wire1, _, wire2, output in gates:
        wire_names.update([wire1, wire2, output])

    # Define symbolic variables
    wire_symbols = {name: symbols(name) for name in wire_names}

    # Build equations
    equations = []
    for wire1, gate_type, wire2, output in gates:
        input_symbols = [wire_symbols[wire1], wire_symbols[wire2]]
        output_symbol = wire_symbols[output]

        if gate_type == "AND":
            equations.append(Eq(output_symbol, input_symbols[0] * input_symbols[1]))
        elif gate_type == "OR":
            equations.append(
                Eq(output_symbol, 1 - (1 - input_symbols[0]) * (1 - input_symbols[1]))
            )
        elif gate_type == "XOR":
            equations.append(
                Eq(
                    output_symbol,
                    input_symbols[0]
                    + input_symbols[1]
                    - 2 * input_symbols[0] * input_symbols[1],
                )
            )
        else:
            raise ValueError(f"Unknown gate type: {gate_type}")

    # Substitute initial values
    substituted_equations = [
        eq.subs({wire_symbols[k]: v for k, v in initial_values.items()})
        for eq in equations
    ]

    # Solve
    solution = solve(substituted_equations)[0]

    # Combine known values with the solution
    final_solution = {
        **solution,
        **{wire_symbols[k]: v for k, v in initial_values.items()},
    }
    return {wire: final_solution[symbol] for wire, symbol in wire_symbols.items()}


def display_schema(
    initial_values: Dict[str, int], gates: List[Tuple[str, str, str, str]]
) -> None:
    # Create a Graphviz graph
    graph = graphviz.Digraph(format="png", engine="dot")

    # Add initial values as nodes (colored for better distinction)
    for wire, value in initial_values.items():
        graph.node(wire, f"{wire} = {value}", shape="ellipse", color="lightblue")

    # Add gates and connect them
    for input1, gate, input2, output in gates:
        graph.node(
            f"{input1}_{gate}_{input2}",
            f"{gate.upper()}",
            shape="rect",
            color="lightgrey",
            style="filled",
            fontcolor="black",
        )
        graph.edge(input1, f"{input1}_{gate}_{input2}")
        graph.edge(input2, f"{input1}_{gate}_{input2}")
        graph.edge(f"{input1}_{gate}_{input2}", output)

    # Render the schema
    graph.render("logic_schema", view=False)
    return


if __name__ == "__main__":
    # Get the graph from the file
    initial_values, gates = get_initial_values_and_gates_from_input_file("./input.txt")

    # Display the schema
    display_schema(initial_values, gates)

    # Create and solve the system of equations
    # Note: easy to implement, slow to solve...
    solution = solve_logic_system(initial_values, gates)

    # Find the magic number
    x_wires = sorted(
        (wire for wire in initial_values if wire.startswith("x")), reverse=True
    )
    y_wires = sorted(
        (wire for wire in initial_values if wire.startswith("y")), reverse=True
    )
    z_wires = sorted((wire for wire in solution if wire.startswith("z")), reverse=True)

    x_bin_value = "".join(str(initial_values[wire]) for wire in x_wires)
    y_bin_value = "".join(str(initial_values[wire]) for wire in y_wires)

    x_value = int(x_bin_value, 2)
    y_value = int(y_bin_value, 2)
    z_value = int("".join(str(solution[wire]) for wire in z_wires), 2)
    z_bin_value = bin(z_value)

    expected_z_value = x_value + y_value
    expected_z_bin_value = bin(expected_z_value)

    print(f"x_value = {x_value}, in bin = {x_bin_value}")
    print(f"y_value = {y_value}, in bin = {y_bin_value}")
    print(f"z_value = {z_value}, in bin = {z_bin_value}")
    print(f"expected_z_value = {expected_z_value}")

    print(z_bin_value[2:])
    print(expected_z_bin_value[2:])

    wrong_bits = expected_z_value ^ z_value
    print(f"{bin(wrong_bits)[2:].zfill(len(z_bin_value)-2)}")

    indices = [i for i, bit in enumerate(reversed(bin(wrong_bits)[2:])) if bit == "1"]
    print(indices)

    print(f"The wires starting with z forms {z_value}")

    # We need to modify the schema to reach a full adder type of schema
    # Visual findings for my inputs
    # z39 need to swap with mqh
    # z28 need to swap with tfb
    # rnq need to swap with bkr
    # vvr need to swap with z08
