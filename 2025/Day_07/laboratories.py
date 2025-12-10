print('== Laboritories ==')


with open('data.txt', 'r', encoding='UTF-8') as data:
    tachyon_manifold =  [[_ for _ in x] for x in data.read().split('\n') if x]
with open('test.txt', 'r', encoding='UTF-8') as test:
    tachyon_manifold_example = [[_ for _ in x] for x in test.read().split('\n') if x]


def run_beam_splitting(manifold):
    start_y = manifold[0].index('S')
    previous_beam = {start_y}
    new_beam = set()
    split = 0
    for row in manifold[1:]:
        for beam in previous_beam:
            if row[beam] == '^':
                split += 1
                row[beam-1] = '|'
                row[beam+1] = '|'
                new_beam.add(beam-1)
                new_beam.add(beam+1)
            else:
                row[beam] = '|'
                new_beam.add(beam)
        previous_beam, new_beam = new_beam, set()
    return split

def solve_many_worlds(manifold):
    # Ensure manifold is a list of lists of characters for mutation safety
    grid = [list(row_str) for row_str in manifold] 
    
    # Find the starting 'S' position (assuming it's in the first row)
    start_y = grid[0].index('S')
    rows = len(grid)
    cols = len(grid[0])
    
    # DP table: paths_count[x][y] stores how many unique ways there are to reach this cell
    paths_count = [[0 for _ in range(cols)] for _ in range(rows)]
    
    # Initialize the starting position with 1 path
    paths_count[0][start_y] = 1

    # Iterate row by row (x) from top to bottom
    for x in range(rows - 1):
        for y in range(cols):
            # If we can reach this cell in the current row
            if paths_count[x][y] > 0:
                count = paths_count[x][y]
                current_char = grid[x][y]
                
                if current_char in ('S', '|'):
                    # Move straight down
                    paths_count[x+1][y] += count
                
                elif current_char == '^':
                    # Split left and right
                    if y > 0:
                        paths_count[x+1][y-1] += count
                    if y < cols - 1:
                        paths_count[x+1][y+1] += count
                
    # The result is the total number of paths summed up in the very last row
    total_ways = sum(paths_count[rows-1])
    return total_ways


print('-- Part 1 --')
print(f'Test: {run_beam_splitting(tachyon_manifold_example)}')
print(f'Data: {run_beam_splitting(tachyon_manifold)}')

print('-- Part 2 --')
print(f'Test: {solve_many_worlds(tachyon_manifold_example)}')
print(f'Data: {solve_many_worlds(tachyon_manifold)}')  # 3156 too low
