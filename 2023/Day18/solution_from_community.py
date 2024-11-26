file_name = 'input.txt'

dig_plan_1 = []
dig_plan_2 = []
for line in open(file_name).read().splitlines():
    direction, count, col = line.split()
    dig_plan_1.append(['RDLU'.index(direction), int(count)])
    dig_plan_2.append([int(col[-2]), int(col[2:-2], 16)])

# Expected solutions
# Sample:    62 /    952408144115
# Data:   48652 /  45757884535661

# Pick's theorem: https://en.wikipedia.org/wiki/Pick%27s_theorem
# inner = Area - (boundary/2) + 1
# Shoelace forumla: https://en.wikipedia.org/wiki/Shoelace_formula
# Area = [shoelace]
offsets = [(1, 0), (0, 1), (-1, 0), (0, -1)]
def make_point(position: tuple[int, int], direction: int, count: int) -> tuple[int, int]:
    return position[0] + offsets[direction][0] * count, position[1] + offsets[direction][1] * count

def shoelace(points):
    x, y = zip(*points)
    return 0.5 * abs(sum(x[i]*y[i+1] - x[i+1]*y[i] for i in range(len(points)-1)))

def solve(data: list[tuple[int, int]]) -> int:
    points = [(0, 0)]
    for direction, count in data:
        points.append(make_point(points[-1], direction, count))
    inner_area = shoelace(points) # The inner area of the "vectors"
    boundary_points = sum(line[1] for line in data) # The points on the border of the "vectors"
    inner_points = int(inner_area) - boundary_points // 2 + 1 # see Pick's theorem
    solution = inner_points + boundary_points 
    return solution

print('Task 1: %d' % solve(dig_plan_1))
print('Task 2: %d' % solve(dig_plan_2))