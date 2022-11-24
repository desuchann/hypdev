'''
Task 28

Create a function that takes a grid of # and -, where each hash (#) represents a
mine and each dash (-) represents a mine-free spot.
Return a grid, where each dash is replaced by a digit, indicating the number of
mines immediately adjacent to the spot i.e. (horizontally, vertically, and diagonally).
'''
from copy import deepcopy

grid = [["-", "-", "-", "#", "#"],
        ["-", "#", "-", "-", "-"],
        ["-", "-", "#", "-", "-"],
        ["-", "#", "#", "-", "-"],
        ["-", "-", "-", "-", "-"]]

# find the dimensions of the grid - an assumption here that it's not ragged
length = len(grid)
width = len(grid[0])

# set up a dictionary that records each mine and its coordinate
grid_coords = [f'{i},{j}' for i in range(length) for j in range(width)]
grid_flatten = [x for y in grid for x in y]
grid_dict = dict(zip(grid_coords, grid_flatten))

# set up an identical grid to fill in with the result
result_dict = deepcopy(grid_dict)

for coords, v in grid_dict.items():
    # leave mines as they are
    if v == '#':
        continue

    # count and record the number of neighbouring mines for each coord
    count = 0
    x, y = coords.split(',')
    x = int(x)
    y = int(y)

    count += 1 if grid_dict.get(f'{x-1},{y-1}') == '#' else 0
    count += 1 if grid_dict.get(f'{x-1},{y}') == '#' else 0
    count += 1 if grid_dict.get(f'{x-1},{y+1}') == '#' else 0

    count += 1 if grid_dict.get(f'{x},{y-1}') == '#' else 0
    count += 1 if grid_dict.get(f'{x},{y+1}') == '#' else 0

    count += 1 if grid_dict.get(f'{x+1},{y-1}') == '#' else 0
    count += 1 if grid_dict.get(f'{x+1},{y}') == '#' else 0
    count += 1 if grid_dict.get(f'{x+1},{y+1}') == '#' else 0

    # save it down
    result_dict[coords] = str(count)

# iteratively put slices of a width equalling the width of the original grid into a list
result_grid = []
start = 0
for _ in range(length):
    result_grid.append(list(result_dict.values())[start:start+width])
    start += length

# print in the correct format
for i in result_grid:
    print(i)
