from math import ceil, floor, prod, sqrt

lines = []
with open("input.txt", "r") as file:
    sheet = file.read().strip()
    lines = sheet.split("\n")

races_durations = lines[0].split(":")[1].strip().split()
races_records = lines[1].split(":")[1].strip().split()

races_durations = [int("".join(races_durations))]
races_records = [int("".join(races_records))]

# distance_traveled(race_duration, press_duration) = press_duration*(race_duration-press_duration)
# We want distance_traveled > race_record
# The equation becomes: press_duration*(race_duration-press_duration) > race_record
# let's define x = press_duration, our variable
# x * (race_duration - x) > race_record
# -x^2 + race_duration*x - race_record > 0
# we note a=-1, b=race_duration and c=-race_record
# We end up with ax^2 + bx + c > 0
# delta = b^2 - 4ac
# solutions are in range ]x1, x2[
# with x1, x2 = -b+- sqrt(delta) / 2a

nb_ways_to_win = [0 for _ in range(len(races_durations))]
for i in range(len(races_durations)):
    race_duration = races_durations[i]
    race_record = races_records[i]

    delta = race_duration**2 - 4 * race_record

    if delta > 0:
        x1 = (-race_duration + sqrt(delta)) / -2
        x2 = (-race_duration - sqrt(delta)) / -2
        min_acceptable_value = ceil(x1) if ceil(x1) != x1 else int(x1 + 1)
        max_acceptable_value = floor(x2) if floor(x2) != x2 else int(x2 - 1)
        nb_ways_to_win[i] = max_acceptable_value - min_acceptable_value + 1

print(prod(nb_ways_to_win))
