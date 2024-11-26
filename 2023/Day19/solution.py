from typing import List, Dict, Tuple, Callable
import re
from functools import reduce


workflows: List[str] = []
part_ratings: List[str] = []

with open("test.txt", "r") as file:
    workflows_str, part_ratings_str = file.read().strip().split("\n\n")
    workflows = workflows_str.strip().split("\n")
    part_ratings = part_ratings_str.strip().split("\n")


workflow_pattern = re.compile(r"(\w+)\{(.+)\}")


more_or_less: Dict[str, Callable[[int, int], bool]] = {
    "<": lambda x, y: x < y,
    ">": lambda x, y: x > y,
}


def parse_workflows_2(workflows_str: List[str]) -> Dict[str, List[Callable]]:
    workflow_dict: Dict[str, List[Callable]] = {}
    for workflow in workflows_str:
        print(f"workflow = {workflow}")
        matched = workflow_pattern.search(workflow)
        if matched:
            workflow_name, rules = matched.groups()
            rules = rules.split(",")
            rules_list: List[Callable] = []
            for rule in rules:
                rule_detail = rule.split(":")
                if len(rule_detail) == 1:
                    rules_list.append(lambda x, rule=rule: [(rule, x)])
                else:
                    operation, destination_workflow = rule_detail
                    rules_list.append(
                        lambda ranges, var=operation[0], op=operation[1], val=int(
                            operation[2:]
                        ), result=destination_workflow: split_range(
                            ranges, var, op, val, result
                        )
                    )
            workflow_dict[workflow_name] = rules_list
    return workflow_dict


def split_range(
    ranges: Dict[str, List[int]], var: str, op: str, val: int, result: str
) -> List[Tuple[str, Dict[str, List[int]]]]:
    split_list: List[Tuple[str, Dict[str, List[int]]]] = []
    new_ranges = ranges.copy()
    value_range = new_ranges[var]
    if value_range[0] < val:
        less = new_ranges.copy()
        less[var] = [value_range[0], val + 1 if op == ">" else val]
        split_list.append(
            (result if more_or_less[op](value_range[0], val) else "", less)
        )
    if value_range[1] > val:
        more = new_ranges.copy()
        more[var] = [val + 1 if op == ">" else val, value_range[1]]
        split_list.append(
            (result if more_or_less[op](value_range[1], val) else "", more)
        )
    return split_list


def find_nb_combo(
    workflow_name: str,
    range_list: List[Dict[str, List[int]]],
    workflows: Dict[str, List[Callable]],
) -> int:
    total = 0
    new_ranges: List[Tuple[str, List[Dict[str, List[int]]]]] = []

    print(f"workflow_name = {workflow_name}")
    for rule in workflows[workflow_name]:
        if not range_list:
            break
        range_split = rule(range_list.pop(0))
        for ranges in range_split:
            if ranges[0] == "":
                range_list.append(ranges[1])
            elif ranges[0] == "A" or ranges[0] == "R":
                if ranges[0] == "A":
                    total += reduce(
                        lambda x, y: x * y,
                        [ranges[1][key][1] - ranges[1][key][0] for key in ranges[1]],
                    )
            else:
                new_ranges.append((ranges[0], [ranges[1]]))
    print(f"new_ranges = {new_ranges}")
    for new_range in new_ranges:
        total += find_nb_combo(*new_range, workflows)
    return total


parsed_workflows = parse_workflows_2(workflows)
start_workflow = "in"
start_range_list = [{"x": [1, 4001], "m": [1, 4001], "a": [1, 4001], "s": [1, 4001]}]
total = find_nb_combo(start_workflow, start_range_list, parsed_workflows)

print(f"total = {total}")
