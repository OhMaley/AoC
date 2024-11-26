import re

almanac = ""
with open("input.txt", "r") as file:
    almanac = file.read().strip()

categories = almanac.split("\n\n")
seeds = []
category_name_to_index = {
    "seed": 0,
    "soil": 1,
    "fertilizer": 2,
    "water": 3,
    "light": 4,
    "temperature": 5,
    "humidity": 6,
    "location": 7,
}
table = [[[] for _ in range(8)] for i in range(8)]

for i, category in enumerate(categories):
    if i == 0:
        # Special treatment for seeds
        seeds = [int(x) for x in re.findall(r"\d+", category)]
    else:
        # Treatment for maps
        map_name, map_content = re.findall(r"(.*?)\s*map:\s*(.*)", category, re.S)[0]
        from_name, to_name = map_name.split("-to-")
        lines = map_content.split("\n")
        m = []
        for line in lines:
            d_range_start, s_range_start, range_len = [int(x) for x in line.split()]
            m.append([d_range_start, s_range_start, range_len])
        table[category_name_to_index[from_name]][category_name_to_index[to_name]] = m

locations = []
for seed in seeds:
    current = seed
    for i in range(7):
        m = table[i][i+1]
        range_to_use = next(filter(lambda r: r[1]<=current<r[1]+r[2], m), None)
        if range_to_use:
            current = range_to_use[0] + current - range_to_use[1]
    locations.append(current)

print(min(locations))
