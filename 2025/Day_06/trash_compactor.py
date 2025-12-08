print('Trash Compactor')

with open('data.txt', 'r', encoding='UTF-8') as data:
    math_problems =  [x for x in data.read().split('\n') if x]
with open('test.txt', 'r', encoding='UTF-8') as test:
    test_math_problems = [x for x in test.read().split('\n') if x]

numbers = [[int(y) for y in x.split() if y] for x in test_math_problems[:-1]]
operators = [x for x in test_math_problems[-1].split() if x]


from itertools import groupby

def group_strings_by_empty(string_list):
    """
    Groups a list of strings into sublists, separating them by empty strings.

    Args:
        string_list: A list of strings, potentially containing empty strings.

    Returns:
        A list of lists, where each inner list contains consecutive non-empty strings.
    """
    grouped_lists = []
    # Group by whether the element is an empty string or not
    for is_not_empty, group in groupby(string_list, key=lambda x: x != ''):
        if is_not_empty:  # If the group consists of non-empty strings
            grouped_lists.append(list(group))
    return grouped_lists


def solve_cephalopod_problems(problems, part_2 = False):
    if part_2:
        total = 0
        numbers = []
        for col in range(len([x for x in problems[0]])):
            number = ''
            for row in range(len(problems[:-1])):
                number = number + problems[row][col] if problems[row][col] else None
            numbers.append(number.strip())
        operators = [x for x in problems[-1].split() if x]
        total = 0
        separated_values = [[int(_) for _ in x] for x in group_strings_by_empty(numbers)]
        for i in range(len(operators)):
            if operators[i] == '*':
                from math import prod
                print(' * '.join(str(v) for v in separated_values[i]))
                total = total if total else 1
                total += prod(separated_values[i])
            else:
                print(' + '.join(str(v) for v in separated_values[i]))
                total += sum(separated_values[i])
        return total
    else:
        numbers = [[int(y) for y in x.split() if y] for x in problems[:-1]]
        operators = [x for x in problems[-1].split() if x]
        total_sum = 0
        for col in range(len(numbers[0])):
            col_sol = 0
            for row in range(len(numbers)):
                if operators[col] == '*':
                    col_sol = col_sol if col_sol else 1
                    col_sol *= numbers[row][col]
                elif operators[col] == '+':
                    col_sol += numbers[row][col]
            total_sum += col_sol
        return total_sum
    

print('-- Part 1 --')
print(f'Test: {solve_cephalopod_problems(test_math_problems)}')
print(f'Data: {solve_cephalopod_problems(math_problems)}')

print('-- Part 2 --')
print(f'Test: {solve_cephalopod_problems([x[::-1] for x in test_math_problems], True)}')
print(f'Data: {solve_cephalopod_problems([x[::-1] for x in math_problems], True)}')