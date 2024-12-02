from typing import List
from itertools import combinations


MIN_DIFF, MAX_DIFF = 1, 3


def get_reports_from_input_file(file_path: str) -> List[List[int]]:
    with open(file_path, "r") as file:
        return [[int(v) for v in line.strip().split()] for line in file]


def is_report_strictly_safe(report: List[int]) -> bool:
    diffs: List[int] = [report[i + 1] - report[i] for i in range(len(report) - 1)]

    is_increasing: bool = all(n >= 0 for n in diffs)
    is_decreasing: bool = all(n <= 0 for n in diffs)
    is_variation_in_bounds: bool = all(MIN_DIFF <= abs(n) <= MAX_DIFF for n in diffs)

    return (is_increasing or is_decreasing) and is_variation_in_bounds


def count_strict_safe_reports(reports: List[List[int]]) -> int:
    return sum(1 for report in reports if is_report_strictly_safe(report))


def count_tolerated_safe_reports(reports: List[List[int]]) -> int:
    total: int = 0
    for report in reports:
        if is_report_strictly_safe(report):
            total += 1
        else:
            # Check all combinations with one level removed from the report
            if any(
                is_report_strictly_safe(list(comb))
                for comb in combinations(report, len(report) - 1)
            ):
                total += 1
    return total


if __name__ == "__main__":
    reports: List[List[int]] = get_reports_from_input_file("./input.txt")

    nb_strict_safe_reports = count_strict_safe_reports(reports)
    print(f"The number of strict safe reports is {nb_strict_safe_reports}")

    nb_tolerated_safe_reports = count_tolerated_safe_reports(reports)
    print(f"The number of tolerated safe reports is {nb_tolerated_safe_reports}")
