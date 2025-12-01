"""Secret Entrance"""
print('== Secret Entrance ==')

with open('data.txt', 'r', encoding='UTF-8') as data:
    puzzle_input =  [x for x in data.read().split('\n') if x]
with open('test.txt', 'r', encoding='UTF-8') as test:
    example = [x for x in test.read().split('\n') if x]


def find_value(input, part_2=False):
    CURRENT_POINT = 50
    ZERO_COUNTER = 0
    PASSING_ZERO = 0
    for x in input:
        direction, value = x[0], int(x[1:])
        delta = value if direction == 'R' else -value
        start = CURRENT_POINT
        end = CURRENT_POINT + delta

        if part_2:
            if end > start:
                # count multiples of 100 strictly between start and end
                PASSING_ZERO += (end - 1) // 100 - start // 100
            elif end < start:
                # symmetric formula for negative delta; exclude start when it's a multiple
                PASSING_ZERO += (start - 1) // 100 - end // 100

        CURRENT_POINT = end % 100
        if CURRENT_POINT == 0:
            ZERO_COUNTER += 1
    return ZERO_COUNTER + PASSING_ZERO

print('-- Part 1 --')
print(f'Test: {find_value(example)}')
print(f'Data: {find_value(puzzle_input)}')

print('-- Part 2 --')
print(f'Test: {find_value(example, part_2=True)}')
print(f'Data: {find_value(puzzle_input, part_2=True)}')