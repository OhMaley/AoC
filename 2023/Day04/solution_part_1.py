import re

cards_instances = {}
card_matching_numbers = {}
max_card_id = 0

with open("input.txt", "r") as file:
    for line in file:
        card, numbers = line.split(":")
        _, card_id = card.split()
        max_card_id = max(max_card_id, int(card_id))
        cards_instances[int(card_id)] = 1
        winning_numbers, numbers_I_have = numbers.split("|")
        winning_numbers = [int(x) for x in re.findall(r"\d+", winning_numbers)]
        numbers_I_have = [int(x) for x in re.findall(r"\d+", numbers_I_have)]
        nb_matching_numbers = len(set(winning_numbers) & set(numbers_I_have))
        card_matching_numbers[int(card_id)] = nb_matching_numbers

for card_id in sorted(card_matching_numbers.keys()):
    nb_matching_numbers = card_matching_numbers[card_id]
    for i in range(card_id + 1, card_id + nb_matching_numbers + 1):
        if i in cards_instances:
            cards_instances[i] += cards_instances[card_id]

sum = sum(cards_instances.values())
print(sum)
