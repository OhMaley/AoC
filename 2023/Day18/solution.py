instructions = []

with open("test.txt", "r") as file:
    instructions = file.read().strip().split("\n")

current = (0, 0)
lagoon = set()
lagoon.add(current)
for instruction in instructions:
    direction, number, color = instruction.split(" ")
    number = int(number)
    if direction == "U":
        lagoon.update([(current[0] - i - 1, current[1]) for i in range(number)])
        current = (current[0] - number, current[1])
    elif direction == "L":
        lagoon.update([(current[0], current[1] - i - 1) for i in range(number)])
        current = (current[0], current[1] - number)
    elif direction == "D":
        lagoon.update([(current[0] + i + 1, current[1]) for i in range(number)])
        current = (current[0] + number, current[1])
    elif direction == "R":
        lagoon.update([(current[0], current[1] + i + 1) for i in range(number)])
        current = (current[0], current[1] + number)
    else:
        print("Wrong direction")

lagoon = list(lagoon)

min_x = min(lagoon, key=lambda x: x[0])[0]
max_x = max(lagoon, key=lambda x: x[0])[0]
min_y = min(lagoon, key=lambda x: x[1])[1]
max_y = max(lagoon, key=lambda x: x[1])[1]
width = max_y - min_y + 1
height = max_x - min_x + 1

for i in range(len(lagoon)):
    lagoon[i] = (lagoon[i][0] - min_x, lagoon[i][1] - min_y)

lagoon_str = ""
for i in range(height):
    for j in range(width):
        c = "."
        if (i, j) in lagoon:
            c = "#"
        lagoon_str += c
    lagoon_str += "\n"
lagoon_str = lagoon_str[:-1]

# print(lagoon_str)
lagoon_lines = lagoon_str.split("\n")
lagoon_grid = [[c for c in line] for line in lagoon_lines]


def get_neighbors(i, j):
    neighbors = [0, 0, 0, 0]  # U, L, D, R
    if i > 0 and lagoon_lines[i - 1][j] == "#":
        neighbors[0] = 1
    if j > 0 and lagoon_lines[i][j - 1] == "#":
        neighbors[1] = 1
    if i < height - 1 and lagoon_lines[i + 1][j] == "#":
        neighbors[2] = 1
    if j < width - 1 and lagoon_lines[i][j + 1] == "#":
        neighbors[3] = 1
    return neighbors


for i, line in enumerate(lagoon_lines):
    inside = False
    for j, c in enumerate(line):
        neighbors = get_neighbors(i, j)
        if c == "#" and neighbors in [[1, 0, 1, 0], [1, 0, 0, 1], [1, 1, 0, 0]]:
            inside = not inside
        else:
            if inside:
                lagoon_grid[i][j] = "#"
        prev = c


def display():
    print("------------------------------")
    for line in lagoon_grid:
        for c in line:
            print(c, end="")
        print()


# display()

total = 0
for line in lagoon_grid:
    for c in line:
        if c == "#":
            total += 1

print(total)
