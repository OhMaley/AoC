import re

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
i = 0
current = "AAA"
while current != "ZZZ":
    instruction = instructions[i % l]
    current = graph[current][0 if instruction == "L" else 1]
    i += 1
print(i)
