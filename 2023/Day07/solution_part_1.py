import re

data = []
with open("input.txt", "r") as file:
    for line in file.read().strip().split("\n"):
        hand, bid = line.split()
        data.append({"hand": hand, "bid": int(bid)})

card_values = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


def second_rule_hand_value(hand):
    value = int("".join(str(card_values[card]).zfill(2) for card in hand)) / 10000000000
    return value


def poker_hand_strength(hand_and_bid):
    hand = hand_and_bid["hand"]
    second_rule_value = second_rule_hand_value(hand)
    cards_counts = {card: hand.count(card) for card in set(hand)}

    if len(cards_counts) == 1:  # Five of a kind
        return 7 + second_rule_value
    elif len(cards_counts) == 2:  # Full House or four of a kind
        if 4 in cards_counts.values():
            return 6 + second_rule_value
        else:
            return 5 + second_rule_value
    elif len(cards_counts) == 3:  # Three of a kind or Two Pairs
        return (
            4 + second_rule_value
            if 3 in cards_counts.values()
            else 3 + second_rule_value
        )
    elif len(cards_counts) == 4:  # One Pair
        return 2 + second_rule_value
    else:
        # High Card
        return 1 + second_rule_value


data.sort(key=poker_hand_strength)
winnings = sum((index + 1) * value["bid"] for index, value in enumerate(data))

print(winnings)
