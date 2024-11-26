from functools import lru_cache


platform = ""

with open("input.txt", "r") as file:
    platform = file.read().strip()

print(platform)
print("--------------")


@lru_cache(maxsize=256)
def rotate_90(s: str, clockwize: bool = True) -> str:
    if clockwize:
        return "\n".join(map("".join, zip(*(s.split())[::-1])))
    return "\n".join([x for x in map("".join, zip(*(s.split())))][::-1])


@lru_cache(maxsize=256)
def tilt_line_left(s: str) -> str:
    new_str = ""
    count = 0
    last_rock_index = -1
    for i, c in enumerate(s):
        if c == "#":
            chunk_indices = [last_rock_index + 1 + j for j in range(count)]
            new_str += "".join("O" for _ in chunk_indices)
            new_str += "".join(
                "." for _ in range(i - last_rock_index - 1 - len(chunk_indices))
            )
            new_str += "#"
            count = 0
            last_rock_index = i
        elif c == "O":
            count += 1
        else:
            pass
    # upper wall
    chunk_indices = [last_rock_index + 1 + j for j in range(count)]
    new_str += "".join("O" for _ in chunk_indices)
    new_str += "".join(
        "." for _ in range(len(s) - last_rock_index - 1 - len(chunk_indices))
    )
    return new_str


@lru_cache(maxsize=256)
def tilt_left(s: str) -> str:
    tilted_rows = []
    for line in s.split("\n"):
        tilted_rows.append(tilt_line_left(line))
    return "\n".join(tilted_rows)


@lru_cache(maxsize=256)
def spin_cycle(s: str) -> str:
    for _ in range(4):
        s = rotate_90(tilt_left(s))
    return s


def compute_load(s: str) -> int:
    sum = 0
    for i, line in enumerate(s.split("\n")[::-1]):
        sum += (i + 1) * line.count("O")
    return sum


platform = rotate_90(platform, False)
nb_cycle = 1000000000
for i in range(nb_cycle):
    platform = spin_cycle(platform)

print(rotate_90(platform))

print(compute_load(rotate_90(platform)))
