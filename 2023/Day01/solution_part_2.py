import re

sum = 0
spelled_digits = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

def digit_to_int_str(d: str):
    if d.isdigit():
       return d
    if d in spelled_digits:
        return str(spelled_digits.index(d) + 1)
    return '0'

with open("input.txt", 'r') as file:
    for line in file:
        digits_str = re.findall(r'\d|(?:one|two|three|four|five|six|seven|eight|nine)', line)
        sum += int(digit_to_int_str(digits_str[0]) + digit_to_int_str(digits_str[-1])) if digits_str else 0
print(sum)