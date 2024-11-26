import re
from math import lcm

instructions = ""
graph = {}

with open("input.txt", "r") as file:
    document = file.read().strip()
    instructions, nodes = document.split("\n\n")
    for node in nodes.split("\n"):
        from_node, to_node_1, to_node_2 = re.findall(
            r"(\w+)\s*=\s*\((\w+),\s*(\w+)\)", node
        )[0]
        graph[from_node] = [to_node_1, to_node_2]

l = len(instructions)


def get_nb_moves(from_node):
    current = from_node
    i = 0
    while current[-1] != "Z":
        instruction = instructions[i % l]
        current = graph[current][0 if instruction == "L" else 1]
        i += 1
    return i


currents = [x for x in graph.keys() if x[-1] == "A"]
nodes_nb_moves = [get_nb_moves(x) for x in currents]

print(lcm(*nodes_nb_moves))
