with open('data.txt', 'r', encoding='UTF-8') as data:
    puzzle_input =  [[_ for _ in x] for x in data.read().split('\n') if x]
with open('test.txt', 'r', encoding='UTF-8') as test:
    example = [[_ for _ in x] for x in test.read().split('\n') if x]


def get_valid_positions(row, col, max_rows, max_cols):
    positions = [(row-1, col), (row+1, col), (row, col-1), (row, col+1), (row-1, col-1), (row-1, col+1), (row+1, col-1), (row+1, col+1)]
    positions = [(r, c) for r, c in positions if 0 <= r < max_rows and 0 <= c < max_cols]
    return positions


def count_accessible_rolls(input):
    total_accessible = set()
    x_len = len(input)
    y_len = len(input[0])
    for row in range(x_len):
        for col in range(y_len):
            neighbors = 0
            if input[row][col] == '@':
                positions = get_valid_positions(row, col, x_len, y_len)
                for r, c in positions:
                    if input[r][c] == '@':
                        neighbors += 1
                if neighbors < 4:
                    total_accessible.add((row, col))
    return total_accessible

print('-- Part 1 --')
print(f'Test: {len(count_accessible_rolls(example))}')
print(f'Data: {len(count_accessible_rolls(puzzle_input))}')

def count_accessible_rolls_part2(input):
    previous_accessible = count_accessible_rolls(input)
    number_removed = 0
    while len(previous_accessible) > 0:
        for row, col in previous_accessible:
            input[row][col] = 'x'
        number_removed += len(previous_accessible)
        previous_accessible = count_accessible_rolls(input)
    return number_removed

print('-- Part 2 --')
print(f'Test: {count_accessible_rolls_part2(example)}')
print(f'Data: {count_accessible_rolls_part2(puzzle_input)}')