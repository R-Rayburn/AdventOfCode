print('Red Nosed Reports')
with open('test.txt', 'r') as test_file:
    test_data = [t for t in test_file.read().split('\n') if t]
with open('data.txt', 'r') as data_file:
    input_data = [d for d in data_file.read().split('\n') if d]

def get_values(data):
    values = [line.split(' ') for line in data]
    return values

def get_safe_sequence(data):
    values = get_values(data)
    safe_count = 0
    for v in values:
        sequence = [abs(int(v[i])-int(v[i+1])) for i in range(len(v)-2)]
        if (sequence == sorted(sequence) or sequence == sorted(sequence)[::-1]) and all(s >= 1 or s <= 3 for s in sequence):
            safe_count += 1
    return safe_count



print(get_safe_sequence(test_data))
print(get_safe_sequence(input_data)) # 255 = too low