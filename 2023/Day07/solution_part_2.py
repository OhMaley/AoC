import re

data = []
with open("input.txt", "r") as file:
    for line in file.read().strip().split("\n"):
        hand, bid = line.split()
        data.append({"hand": hand, "bid": int(bid)})

card_values = {
    "J": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "Q": 12,
    "K": 13,
    "A": 14,
}


def second_rule_hand_value(hand):
    value = int("".join(str(card_values[card]).zfill(2) for card in hand)) / 10000000000
    return value


def hand_type_score(hand):
    cards_counts = {card: hand.count(card) for card in set(hand)}
    if len(cards_counts) == 1:  # Five of a kind
        return 7
    elif len(cards_counts) == 2:  # Full House or four of a kind
        if 4 in cards_counts.values():
            return 6
        else:
            return 5
    elif len(cards_counts) == 3:  # Three of a kind or Two Pairs
        return 4 if 3 in cards_counts.values() else 3
    elif len(cards_counts) == 4:  # One Pair
        return 2
    else:
        # High Card
        return 1


def poker_hand_strength(hand_and_bid):
    hand = hand_and_bid["hand"]

    best_score = hand_type_score(hand)
    if "J" in hand:
        for card in "".join(set(hand.replace("J", ""))):
            new_hand = hand.replace("J", card)
            best_score = max(best_score, hand_type_score(new_hand))

    return best_score + second_rule_hand_value(hand)


data.sort(key=poker_hand_strength)
winnings = sum((index + 1) * value["bid"] for index, value in enumerate(data))

print(winnings)
