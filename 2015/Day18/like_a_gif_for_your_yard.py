with open('data.txt', 'r') as file:
    containers = file.read().split('\n')

with open('test.txt', 'r') as test_file:
    test_containers = test_file.read().split('\n')

def get_neighbor_positions(x, y, max_x, max_y):
    positions = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < max_x and 0 <= ny < max_y:
                positions.append((nx, ny))
    return positions

def switch_lights(current_state, new_state, sticky_corners=False):
    
    for i in range(len(current_state)):
        for j in range(len(current_state[0])):
            corner_condition = (i, j) in [(0, 0), (0, len(current_state[0]) - 1), (len(current_state) - 1, 0), (len(current_state) - 1, len(current_state[0]) - 1)]
            # if sticky_corners and corner_condition:
            #     new_state[i][j] = '#'
            #     continue
            current_point = current_state[i][j]
            neighbor_positions = get_neighbor_positions(i, j, len(current_state), len(current_state[0]))
            surrounding_lights_on = sum(1 for x, y in neighbor_positions if current_state[x][y] == '#')
            if current_point == '.' and surrounding_lights_on == 3:
                new_state[i][j] = '#'
            elif sticky_corners and corner_condition:
                new_state[i][j] = '#'
            elif current_point == '#' and surrounding_lights_on not in [2, 3]:
                new_state[i][j] = '.'
            else:
                new_state[i][j] = current_point
    return new_state

def like_a_gif_for_your_yard(containers, steps=100, sticky_corners=False):
    current_state = [list(row) for row in containers]
    new_state = [row.copy() for row in current_state]
    if sticky_corners:
        current_state[0][0] = '#'
        current_state[0][len(current_state[0]) - 1] = '#'
        current_state[len(current_state) - 1][0] = '#'
        current_state[len(current_state) - 1][len(current_state[0]) - 1] = '#'

    for _ in range(steps):
        # print('\n')
        # print('\n'.join(''.join(row) for row in current_state))
        new_state = switch_lights(current_state, new_state, sticky_corners)
        current_state, new_state = new_state, current_state
    # print('\n')
    # print('\n'.join(''.join(row) for row in current_state))
    return sum(row.count('#') for row in current_state)

print('--- Part 1 ---')
print(f'Test: {like_a_gif_for_your_yard(test_containers, 4)}')
print(f'Data: {like_a_gif_for_your_yard(containers, 100)}')
print('--- Part 2 ---')
print(f'Test: {like_a_gif_for_your_yard(test_containers, 6, sticky_corners=True)}')
print(f'Data: {like_a_gif_for_your_yard(containers, 100, sticky_corners=True)}')