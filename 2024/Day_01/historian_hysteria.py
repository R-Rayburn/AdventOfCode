print('Historian Hysteria')

with open('test.txt', 'r') as test_file:
    test_data = [t for t in test_file.read().split('\n') if t]
with open('data.txt', 'r') as data_file:
    input_data = [d for d in data_file.read().split('\n') if d]

def get_values(data):
    values = (line.split(' ') for line in data)
    return [[v[0], v[-1]] for v in values]

def get_distance_of_ordered_list(data):
    values = get_values(data)
    print(values)
    lhs = sorted([int(v[0]) for v in values], key=lambda x: int(x))
    rhs = sorted([int(v[1]) for v in values], key=lambda x: int(x))
    total_distance = 0
    for i in range(len(values)):
        total_distance += abs(lhs[i]-rhs[i])
    return total_distance

print('Part 1')
print(f'Test: {get_distance_of_ordered_list(test_data)}')
print(f'Data: {get_distance_of_ordered_list(input_data)}')

print('Part 2')
# find count