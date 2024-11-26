import re

sum = 0
with open("input.txt", 'r') as file:
    for line in file:
        digits_str = re.findall(r'\d', line)
        sum += int(digits_str[0] + digits_str[-1]) if digits_str else 0
print(sum)