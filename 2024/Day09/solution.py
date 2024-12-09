from typing import List, Deque
from collections import defaultdict, Counter, deque


def get_disk_map_from_input_file(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read().strip()


def unpack(disk_map: str) -> str:
    unpack_disk_map = ""
    free_char = chr(0x10FFFF)
    for i, c in enumerate(disk_map):
        is_file = i % 2 == 0
        file_id = i // 2
        size = int(c)
        unpack_disk_map += (chr(file_id) if is_file else free_char) * size
    return unpack_disk_map


def defragment(unpack_disk_map: str) -> str:
    defragmented_disk_map = ""
    size = len(unpack_disk_map)
    index_forward = 0
    index_backward = size - 1
    free_char = chr(0x10FFFF)

    while index_forward <= index_backward:
        c = unpack_disk_map[index_forward]
        if c == free_char:
            next_char = unpack_disk_map[index_backward]
            while next_char == free_char:
                index_backward -= 1
                next_char = unpack_disk_map[index_backward]
            defragmented_disk_map += next_char
            index_backward -= 1
        else:
            defragmented_disk_map += c
        index_forward += 1

    return defragmented_disk_map


def defragment_block(disk_map: str) -> str:
    unpack_disk_map = deque([])
    free_spaces = deque([])
    file_id = 0
    defragmented_disk_map = []
    position = 0
    free_char = chr(0x10FFFF)

    # Unpack the disk map
    for i, c in enumerate(disk_map):
        is_file = i % 2 == 0
        if is_file:
            unpack_disk_map.append((position, int(c), file_id))
            for i in range(int(c)):
                defragmented_disk_map.append(chr(file_id))
                position += 1
            file_id += 1
        else:
            free_spaces.append((position, int(c)))
            for i in range(int(c)):
                defragmented_disk_map.append(free_char)
                position += 1

    # Defragment the disk map by block
    for position, block_size, file_id in reversed(unpack_disk_map):
        for space_index, (space_position, space_size) in enumerate(free_spaces):
            if space_position < position and block_size <= space_size:
                for i in range(block_size):
                    defragmented_disk_map[position + i] = free_char
                    defragmented_disk_map[space_position + i] = chr(file_id)
                free_spaces[space_index] = (
                    space_position + block_size,
                    space_size - block_size,
                )
                break

    return "".join(defragmented_disk_map)


def compute_checksum(defragmented_disk_map: str) -> int:
    free_char = chr(0x10FFFF)
    return sum(
        i * ord(c) for i, c in enumerate(defragmented_disk_map) if c != free_char
    )


if __name__ == "__main__":
    disk_map = get_disk_map_from_input_file("./input.txt")

    # Defragment byte by byte
    unpack_disk_map = unpack(disk_map)
    defragmented_disk_map = defragment(unpack_disk_map)
    checksum = compute_checksum(defragmented_disk_map)
    print(f"The filesystem checksum is {checksum}")

    # Defragment block by block
    defragmented_disk_map = defragment_block(disk_map)
    checksum = compute_checksum(defragmented_disk_map)
    print(f"The filesystem checksum is {checksum}")
