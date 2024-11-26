patterns = []

with open("input.txt", "r") as file:
    patterns = file.read().strip().split("\n\n")


def find_reflection_line(pattern: str, diff: int = 0):
    lines = pattern.split("\n")
    transposed_lines = ["".join(row) for row in list(map(list, zip(*lines)))]

    for i, input_lines in enumerate([lines, transposed_lines]):
        is_vertical = i != 0

        size = len(input_lines)
        for i in range(size - 1):
            chunk_size = min(i + 1, size - i - 1)
            c1 = input_lines[max(0, i + 1 - chunk_size) : i + 1]
            c2 = input_lines[i + chunk_size : i : -1]
            nb_diff = sum(1 for a, b in zip("".join(c1), "".join(c2)) if a != b)
            if nb_diff == diff:
                return i, is_vertical
    return -1, True


total = 0
for pattern in patterns:
    # print("-----------------")
    # print(pattern)
    # print("-----------------")

    reflection_line_index, is_vertical = find_reflection_line(pattern, 1)
    total += (1 if is_vertical else 100) * (reflection_line_index + 1)
    # print(reflection_line_index, is_vertical)

print(total)
