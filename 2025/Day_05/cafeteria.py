
with open('data.txt', 'r', encoding='UTF-8') as data:
    puzzle_fresh_ranges, puzzle_ingredient_ids =  [x for x in data.read().split('\n\n') if x]
with open('test.txt', 'r', encoding='UTF-8') as test:
    example_fresh_ranges, example_ingredient_ids = [x for x in test.read().split('\n\n') if x]


def set_up_data(ranges, ids):
    return [[int(y) for y in x.split('-')] for x in ranges.split('\n')], ids.split('\n')

example_fresh_ranges, example_ingredient_ids = set_up_data(example_fresh_ranges, example_ingredient_ids)
puzzle_fresh_ranges, puzzle_ingredient_ids = set_up_data(puzzle_fresh_ranges, puzzle_ingredient_ids)

def collect_safe_ingredient_ids(ranges):
    safe_ids = set()
    for r in ranges:
        safe_ids.update(x for x in range(int(r[0]), int(r[1])+1))
    return safe_ids


def check_inventory(ranges, ids):
    safe_count = 0
    for id in ids:
        for range in ranges:
            if int(range[0]) <= int(id) <= int(range[1]) or \
                int(range[1]) <= int(id) <= int(range[0]):
                safe_count += 1
                break
    return safe_count

print('Part 1:')
print(f'Example: {check_inventory(example_fresh_ranges, example_ingredient_ids)}')
print(f'Data: {check_inventory(puzzle_fresh_ranges, puzzle_ingredient_ids)}')

def combine_ranges(id_ranges):
    lhs_rhs_dict = {}
    for key, value in id_ranges:
        if key in lhs_rhs_dict.keys():
            lhs_rhs_dict[key] = max([value, lhs_rhs_dict[key]])
        else:
            lhs_rhs_dict[key] = value
    for key_1 in lhs_rhs_dict.keys():
        if lhs_rhs_dict[key_1] == None:
            continue
        for key_2 in lhs_rhs_dict.keys():
            if key_1 == key_2 or lhs_rhs_dict[key_2] == None:
                continue
            elif key_1 <= key_2 <= lhs_rhs_dict[key_2] <= lhs_rhs_dict[key_1]:
                lhs_rhs_dict[key_2] = None
            elif key_1 <= key_2 <= lhs_rhs_dict[key_1] <= lhs_rhs_dict[key_2]:
                lhs_rhs_dict[key_1] = lhs_rhs_dict[key_2]
                lhs_rhs_dict[key_2] = None
            elif key_2 <= key_1 <= lhs_rhs_dict[key_1] <= lhs_rhs_dict[key_2]:
                lhs_rhs_dict[key_1] = None
                break
            elif key_2 <= key_1 <= lhs_rhs_dict[key_2] <= lhs_rhs_dict[key_1]:
                lhs_rhs_dict[key_2] = lhs_rhs_dict[key_1]
                lhs_rhs_dict[key_1] = None
                break
    return sum([abs(key - value) + 1 for key, value in lhs_rhs_dict.items() if value is not None])

print('Part 2')
print('Example:', combine_ranges(example_fresh_ranges))
print('Data:', combine_ranges(puzzle_fresh_ranges))
