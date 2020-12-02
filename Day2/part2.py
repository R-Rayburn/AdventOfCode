f = open("data.txt", 'r')

valid_passwords = 0
number_of_passwords = 0
invalid_passwords = 0

for line in f:
    policy, pwd = line.split(':')
    p_range, p_char = policy.split(' ')
    minimum, maximum = p_range.split('-')

    if (pwd.strip()[int(minimum)-1] == p_char) ^ (pwd.strip()[int(maximum)-1] == p_char):
        valid_passwords += 1
    else:
        invalid_passwords += 1
    number_of_passwords += 1

print('valid_passwords: ', valid_passwords)
print('invalid_passwords: ', invalid_passwords)
print('number_of_passwords: ', number_of_passwords)
