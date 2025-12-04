print('== Lobby Layout ==')

with open('data.txt', 'r', encoding='UTF-8') as data:
    puzzle_input =  [x for x in data.read().split('\n') if x]
with open('test.txt', 'r', encoding='UTF-8') as test:
    example = [x for x in test.read().split('\n') if x]

def find_black_tiles(input, part_2=False):
    directions = {
        'e': (1, 0),
        'se': (0, -1),
        'sw': (-1, -1),
        'w': (-1, 0),
        'nw': (0, 1),
        'ne': (1, 1),
    }

    black_tiles = set()

    for line in input:
        x, y = 0, 0
        i = 0
        while i < len(line):
            if line[i] in ('e', 'w'):
                dir_ = line[i]
                i += 1
            else:
                dir_ = line[i:i+2]
                i += 2
            dx, dy = directions[dir_]
            x += dx
            y += dy
        if (x, y) in black_tiles:
            black_tiles.remove((x, y))
        else:
            black_tiles.add((x, y))

    if not part_2:
        return len(black_tiles)

    for _ in range(100):
        neighbor_counts = {}
        for x, y in black_tiles:
            for dx, dy in directions.values():
                neighbor = (x + dx, y + dy)
                neighbor_counts[neighbor] = neighbor_counts.get(neighbor, 0) + 1

        new_black_tiles = set()
        for tile, count in neighbor_counts.items():
            if tile in black_tiles and count in (1, 2):
                new_black_tiles.add(tile)
            elif tile not in black_tiles and count == 2:
                new_black_tiles.add(tile)
        black_tiles = new_black_tiles

    return len(black_tiles)

print('-- Part 1 --')
print(f'Test: {find_black_tiles(example)}')
print(f'Data: {find_black_tiles(puzzle_input)}')

print('-- Part 2 --')
print(f'Test: {find_black_tiles(example, part_2=True)}')
print(f'Data: {find_black_tiles(puzzle_input, part_2=True)}')