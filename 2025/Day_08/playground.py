
with open('data.txt', 'r', encoding='UTF-8') as data:
    junction_boxes =  [tuple(int(x) for x in box.split(',')) for box in data.read().split('\n') if box]
with open('test.txt', 'r', encoding='UTF-8') as test:
    example_junction_boxes = [tuple(int(x) for x in box.split(',')) for box in test.read().split('\n') if box]

def euclidean_distance(point_1, point_2):
    from math import sqrt
    return sqrt((abs(point_1[0]-point_2[0]) ** 2) + (abs(point_1[1]-point_2[1]) ** 2) + (abs(point_1[2]-point_2[2]) ** 2))

def map_boxes(boxes):
    box_mapping = {key: dict() for key in boxes}
    for key in box_mapping.keys():
        box_mapping[key] = {k: euclidean_distance(key, k) for k in box_mapping if k != key}
    return box_mapping

def make_connections(boxes, iterrations):
    connected_boxes = []
    box_dict = map_boxes(boxes)
    # TODO: get minimum box dict to just iterrate over
    # euclidean_distance_map = dict()
    # for point_1, value in box_dict.items():
    #     for point_2, v in value.items():
    #         if v in euclidean_distance_map.keys():
    #             euclidean_distance_map[v].update([point_1, point_2])
    #         else:
    #             euclidean_distance_map[v] = set([point_1, point_2])
    # for key in euclidean_distance_map.keys():
    #     print('key:', key, ' ', euclidean_distance_map[key])

    for _ in range(iterrations):
        minimum_boxes = dict()
        for box, box_distances in box_dict.items():
            minimum_boxes[box] = {key: value for key, value in box_distances.items() if value == min(box_distances.values())}
        # short_item = []
        # for key, value in minimum_boxes.items():
        #     v_values = value.values()
        #     if v_values[0] == min(value.values()):
        #         short_item.append(key)
        # print(short_item)
        short_items = [key for key, value in minimum_boxes.items() if list(value.values())[0] == min([_ for v in minimum_boxes.values() for _ in v.values()])]
        # print(short_items)
        if len(connected_boxes) == 0:
            connected_boxes.append(tuple(short_items))
            # print('connected_boxes:', connected_boxes)
            point_1, point_2 = short_items
            box_dict[point_1].pop(point_2)
            box_dict[point_2].pop(point_1)
        else:
            was_added = False
            for i in range(len(connected_boxes)):
                if (short_items[0] in connected_boxes[i] or short_items[1] in connected_boxes[i]) and not (short_items[0] in connected_boxes[i] and short_items[1] in connected_boxes[i]):
                    connected_boxes[i] = tuple(set(connected_boxes[i] + tuple(short_items)))
                    point_1, point_2 = short_items
                    box_dict[point_1].pop(point_2)
                    box_dict[point_2].pop(point_1)
                    was_added = True
                    break
            if not was_added:
                connected_boxes.append(tuple(short_items))
                point_1, point_2 = short_items
                box_dict[point_1].pop(point_2)
                box_dict[point_2].pop(point_1)
            # print(connected_boxes)

        # for key in minimum_boxes.keys():
            # print(f'{key}: {minimum_boxes[key]}')
        # print(short_items)
        print(len(connected_boxes))
    return connected_boxes
            


print(make_connections(example_junction_boxes, 11))
print(make_connections(junction_boxes, 1001))