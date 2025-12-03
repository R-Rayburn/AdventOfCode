print('-- LOBBY --')

with open('data.txt', 'r', encoding='UTF-8') as data:
    puzzle_input =  [x for x in data.read().split('\n') if x]
with open('test.txt', 'r', encoding='UTF-8') as test:
    example = [x for x in test.read().split('\n') if x]


def find_max_voltage(input):
    largest_voltage = max([int(x) for x in input[:len(input)-1]])
    l_v_index = [int(x) for x in input].index(largest_voltage)
    rhs = input[l_v_index + 1:]
    next_largest_voltage = max([int(x) for x in rhs])
    return int(str(largest_voltage) + str(next_largest_voltage))

def find_max_voltage_part_2(input):
    current_voltage = ''
    current_cutoff = 12
    while len(current_voltage) < 12:
        largest_voltage = max([int(x) for x in input[:len(input)-current_cutoff+1]])
        l_v_index = [int(x) for x in input].index(largest_voltage)
        current_voltage += str(largest_voltage)
        input = input[l_v_index + 1:]
        current_cutoff = 12 - len(current_voltage)
    return int(current_voltage)

def find_total_voltage(input, part_2=False):
    return sum([find_max_voltage(x) for x in input]) if not part_2 else sum([find_max_voltage_part_2(x) for x in input])

print('-- Part 1 --')
print(f'Test: {find_total_voltage(example)}')
print(f'Data: {find_total_voltage(puzzle_input)}')

print('-- Part 2 --')
print(f'Test: {find_total_voltage(example, part_2=True)}')
print(f'Data: {find_total_voltage(puzzle_input, part_2=True)}')