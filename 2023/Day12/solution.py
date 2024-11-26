from itertools import product

records = ""

with open("test.txt", "r") as file:
    records = file.read().strip().split("\n")


def springs_is_valid(springs: str, valid_info: list[int]):
    count = 0
    info_index = 0
    for c in springs:
        if c == "#":
            count += 1
        elif count > 0:
            if info_index < len(valid_info) and count != valid_info[info_index]:
                return False
            count = 0
            info_index += 1
    if count > 0:
        if info_index < len(valid_info) and count != valid_info[info_index]:
            return False
        info_index += 1
    if info_index == len(valid_info):
        return True
    return False


def count_valid_springs_possibilities(springs, contiguous_dmg_info):
    unknown_indices = [i for i, c in enumerate(springs) if c == "?"]
    nb_possibilities = 0
    for combination in product(".#", repeat=len(unknown_indices)):
        possible_springs = list(springs)
        for i, c in zip(unknown_indices, combination):
            possible_springs[i] = c
        possible_springs = "".join(possible_springs)
        if springs_is_valid(possible_springs, contiguous_dmg_info):
            nb_possibilities += 1
    return nb_possibilities


def fast_count_valid_springs_possibilities(springs, contiguous_dmg_info):
    current_count = 0
    possibilities_count = [1] + [0] * max(contiguous_dmg_info)

    for i in range(len(springs)):
        if springs[i] == "#":
            current_count += 1
        elif springs[i] == "?":
            # for count in range(len(possibilities_count) - 1, current_count - 1, -1):
            for count in range(current_count, -1, -1):
                possibilities_count[count] += possibilities_count[count - 1]
                # possibilities_count[count] += possibilities_count[count - current_count]
            current_count = 0
        else:
            current_count = 0

    nb_possibilities = 1
    for count in contiguous_dmg_info:
        nb_possibilities *= possibilities_count[count]

    return nb_possibilities


possibilities = []
for record in records:
    springs, contiguous_dmg_info = record.split(" ")
    contiguous_dmg_info = [int(x) for x in contiguous_dmg_info.split(",")]

    unknown_indices = [i for i, c in enumerate(springs) if c == "?"]

    # nb_possibilities = count_valid_springs_possibilities(springs, contiguous_dmg_info)
    nb_possibilities = fast_count_valid_springs_possibilities(springs, contiguous_dmg_info)
    possibilities.append(nb_possibilities)

print(sum(possibilities))
