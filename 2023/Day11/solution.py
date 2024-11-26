space_image = ""

with open("input.txt", "r") as file:
    space_image = file.read().strip()

# print(space_image)

width = 0
galaxies_cols = []
galaxies_rows = []
for i, line in enumerate(space_image.split("\n")):
    width = max(width, len(line))
    galaxies_in_line = [j for j, c in enumerate(line) if c == "#"]
    if galaxies_in_line:
        galaxies_rows += [i for _ in range(len(galaxies_in_line))]
        galaxies_cols += galaxies_in_line

sorted_galaxies_rows = sorted(galaxies_rows)
sorted_galaxies_cols = sorted(galaxies_cols)


def apply_expansion(l, factor):
    gap = 0
    prev = 0
    for i, v in enumerate(l):
        if v - prev > 1:
            gap += (v - prev - 1) * factor
        l[i] = v + gap
        prev = v


def sum_pairs(l):
    n = len(l)
    sum = 0
    for i in range(n - 1):
        sum += (i + 1) * (n - i - 1) * (l[i + 1] - l[i])
    return sum


apply_expansion(sorted_galaxies_rows, 1000000-1)
apply_expansion(sorted_galaxies_cols, 1000000-1)


sum_rows = sum_pairs(sorted_galaxies_rows)
sum_cols = sum_pairs(sorted_galaxies_cols)

print(sum_rows + sum_cols)
