import re


initialization_sequence = ""

with open("input.txt", "r") as file:
    initialization_sequence = file.read().strip()

steps = initialization_sequence.split(",")
step_pattern = re.compile(r"(\D+)(-|=)(\d?)")
boxes = [[] for _ in range(256)]  # Contains list of list [<label>, <focal>]


def hash(s: str) -> int:
    current_value = 0
    for c in s:
        current_value = ((current_value + ord(c)) * 17) % 256
    return current_value


def remove_lens(from_box_index: int, lens_label: str) -> None:
    boxes[from_box_index] = [x for x in boxes[from_box_index] if x[0] != lens_label]


def add_lens(to_box_index: int, lens_label: str, lens_focal: int) -> None:
    for i, lens in enumerate(boxes[to_box_index]):
        if lens[0] == lens_label:
            boxes[to_box_index][i][1] = lens_focal
            break
    else:
        boxes[to_box_index].append([lens_label, lens_focal])


for step in steps:
    search_result = step_pattern.search(step)
    if search_result:
        label, operation, op_arg = search_result.groups()
        box_index = hash(label)
        if operation == "-":
            remove_lens(box_index, label)
        elif operation == "=":
            add_lens(box_index, label, int(op_arg))

        # print(label, operation, op_arg)
        # for i, box in enumerate(boxes):
        #     if box:
        #         print(f"Box {i}: {box}")

total = sum(
    (i + 1) * (j + 1) * lens[1]
    for i, box in enumerate(boxes)
    for j, lens in enumerate(box)
)
print(total)
