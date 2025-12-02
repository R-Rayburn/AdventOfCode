import re

with open('data.txt', 'r', encoding='UTF-8') as data:
    puzzle_input =  [x for x in data.read().split(',') if x]
with open('test.txt', 'r', encoding='UTF-8') as test:
    example = [x for x in test.read().split(',') if x]

def find_invalid_ids_sum(input, part_2=False):
    invalid_ids = []
    repeating_single_regex = re.compile(r'^(\d)\1+$')
    repeating_regex = re.compile(r'^(\d{2})\1+$')
    for id_range in input:
        start, end = [int(i) for i in id_range.split('-')]
        id_list = list(range(start, end + 1))
        for id_num in id_list:
            str_id = str(id_num)
            if (part_2):
                for x in range(1, len(str_id)//2 + 1):
                    repeating_regex = re.compile(rf'^(\d{{{x}}})\1+$')
                    if repeating_regex.search(str_id):
                        invalid_ids.append(id_num)
                        break                
            elif len(str_id) % 2 == 0:
                if str_id[:len(str_id)//2] == str_id[len(str_id)//2:]:
                    invalid_ids.append(id_num)
    return sum(invalid_ids)

print('-- Part 1 --')
print(f'Test: {find_invalid_ids_sum(example)}')
print(f'Data: {find_invalid_ids_sum(puzzle_input)}')

print('-- Part 2 --')
print(f'Test: {find_invalid_ids_sum(example, part_2=True)}')
print(f'Data: {find_invalid_ids_sum(puzzle_input, part_2=True)}')