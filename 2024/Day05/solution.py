from typing import List, Tuple, Dict, Set
from collections import defaultdict
from functools import cmp_to_key


def get_rules_and_updates_from_input(
    file_path: str,
) -> Tuple[List[List[int]], List[List[int]]]:
    with open(file_path, "r") as file:
        rules_str: str
        updates_str: str
        rules_str, updates_str = file.read().strip().split("\n\n")

        rules: List[List[int]] = [
            list(map(int, rule.split("|"))) for rule in rules_str.strip().split("\n")
        ]
        updates: List[List[int]] = [
            list(map(int, update.split(",")))
            for update in updates_str.strip().split("\n")
        ]

        return rules, updates


def construct_graph(pairs: List[List[int]]) -> Dict[int, Set[int]]:
    graph = defaultdict(set)
    for a, b in pairs:
        graph[a].add(b)
    return graph


def is_correctly_sorted(lst: List[int], graph: Dict[int, Set[int]]) -> bool:
    for i in range(len(lst) - 1):
        if (
            lst[i + 1] in graph[lst[i]]
        ):  # Check if there's a valid edge lst[i] -> lst[i+1]
            continue
        return False
    return True


def compare(graph: Dict[int, Set[int]], a: int, b: int) -> int:
    if b in graph[a]:
        return -1
    elif a in graph[b]:
        return 1
    else:
        return 0


if __name__ == "__main__":
    page_ordeing_rules: List[List[int]]
    pages_to_produce_in_each_update: List[List[int]]

    page_ordering_rules, pages_to_produce_in_each_update = (
        get_rules_and_updates_from_input("./input.txt")
    )

    # Construct a graph from the rules
    graph = construct_graph(page_ordering_rules)

    # Sum the middle page number of all correctly sorted updates
    sum_middle_page_numbers = sum(
        update[len(update) // 2]
        for update in pages_to_produce_in_each_update
        if is_correctly_sorted(update, graph)
    )
    print(f"Sum of already correctly sorted updates is {sum_middle_page_numbers}")

    # Sort incorrect sorted updates
    sum_middle_page_numbers = 0
    for update in pages_to_produce_in_each_update:
        if not is_correctly_sorted(update, graph):
            sorted_update = sorted(
                update, key=cmp_to_key(lambda a, b: compare(graph, a, b))
            )
            sum_middle_page_numbers += sorted_update[len(sorted_update) // 2]
    print(f"Sum of corrected incorrectly-sorted updates {sum_middle_page_numbers}")
