card_subject_number = 7
door_subject_number = 7
card_public_key = 9033205
door_public_key = 9281649

value = 1
card_loop_size = 0
while value != card_public_key:
    value *= card_subject_number
    value %= 20201227
    card_loop_size += 1
print(f"Card loop size is: {card_loop_size}")

value = 1
door_loop_size = 0
while value != door_public_key:
    value *= door_subject_number
    value %= 20201227
    door_loop_size += 1
print(f"Door loop size is: {door_loop_size}")
# once we have the loop sizes, we can determine the encryption key
value = 1
for _ in range(door_loop_size):
    value *= card_public_key
    value %= 20201227
print(f"Encryption key is: {value}")
value = 1
for _ in range(card_loop_size):
    value *= door_public_key
    value %= 20201227
print(f"Encryption key is: {value}")
