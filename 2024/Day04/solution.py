from typing import List


def get_word_search_from_input_file(file_path: str) -> List[str]:
    with open(file_path, "r") as file:
        return file.read().strip().split("\n")


def count_occurences(word: str, table: List[str]) -> int:
    count: int = 0

    # Count horizontal occurences
    count += count_horizontal_occurences(word, table)

    # Count vertical occurences
    count += count_vertical_occurences(word, table)

    # Count diagonals occurences
    count += count_diagonals_occurences(word, table)

    return count


def count_horizontal_occurences(word: str, table: List[str]) -> int:
    return sum(line.count(word) + line.count(word[::-1]) for line in table)


def count_vertical_occurences(word: str, table: List[str]) -> int:
    transpose_table: List[str] = ["".join(row) for row in zip(*table)]
    return sum(line.count(word) + line.count(word[::-1]) for line in transpose_table)


def count_diagonals_occurences(word: str, table: List[str]) -> int:
    count: int = 0

    # Positive diagonals
    positive_diagonals: List[str] = get_positive_diagonals(table)
    count += sum(diagonal.count(word) for diagonal in positive_diagonals)
    count += sum(diagonal.count(word[::-1]) for diagonal in positive_diagonals)

    # Negative diagonals
    rotated_table: List[str] = ["".join(row) for row in zip(*table[::-1])]
    negative_diagonals: List[str] = get_positive_diagonals(rotated_table)
    count += sum(diagonal.count(word) for diagonal in negative_diagonals)
    count += sum(diagonal.count(word[::-1]) for diagonal in negative_diagonals)

    return count


def get_positive_diagonals(table: List[str]) -> List[str]:
    height: int = len(table)
    width: int = len(table[0])
    positive_diagonals: List[str] = []

    for col in range(width):
        diagonal: str = ""
        for row, c in enumerate(range(col, -1, -1)):
            if row < height and c < width:
                diagonal += table[row][c]
        positive_diagonals.append(diagonal)
    for row in range(1, height):
        diagonal: str = ""
        for r, col in enumerate(range(width - 1, -1, -1)):
            if row + r < height and col < width:
                diagonal += table[row + r][col]
        positive_diagonals.append(diagonal)

    return positive_diagonals


def count_cross_occurences(word: str, table: List[str]) -> int:
    word_length = len(word)
    if word_length % 2 == 0:
        return 0

    count: int = 0
    height: int = len(table)
    width: int = len(table[0])
    middle_index = word_length // 2
    middle_char = word[middle_index]

    for i in range(middle_index, height - middle_index):
        for j in range(middle_index, width - middle_index):
            if middle_char == table[i][j]:
                row_start = max(0, i - middle_index)
                row_end = min(height, i + middle_index + 1)
                col_start = max(0, j - middle_index)
                col_end = min(width, j + middle_index + 1)
                sub_table = [
                    "".join(row[col_start:col_end]) for row in table[row_start:row_end]
                ]
                count += 1 if is_cross_here(sub_table, word) else 0

    return count


def is_cross_here(table: List[str], word: str) -> bool:
    size: int = len(word)
    positive_diagonal: str = "".join(table[size - i - 1][i] for i in range(size))
    negative_diagonal: str = "".join(table[i][i] for i in range(size))
    return (word in positive_diagonal or word[::-1] in positive_diagonal) and (
        word in negative_diagonal or word[::-1] in negative_diagonal
    )


if __name__ == "__main__":
    word_search: List[str] = get_word_search_from_input_file("./input.txt")

    count: int = count_occurences("XMAS", word_search)
    print(f"'XMAS' appears {count} times")

    count = count_cross_occurences("MAS", word_search)
    print(f"'Cross MAS' appears {count} times")
