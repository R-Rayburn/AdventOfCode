from math import sqrt

file_name = 'data.txt'

with open(file_name, 'r') as f:
    data = [x.split('\n') for x in f.read().split('\n\n') if x]


# print(data)
# data_map = {}
# for d in data:
#     id = int(''.join([x for x in d[0] if x.isdigit()]))
#     tile = d[1:]
#     data_map[id] = tile
#     # camera_tiles.append(CameraTile(id, tile))

# for k, v in data_map.items():
#     print(f'ID: {k}')
#     for row in v:
#         print(row)
#     print('-----')


class CameraTile:
    def __init__(self, id, tile):
        self.id = id
        self.tile = tile
        self.neighbors = []
        self.top = None
        self.bottom = None
        self.left = None
        self.right = None
        self.point = None

    def rotate(self):
        self.tile = [''.join(x) for x in list(zip(*self.tile[::-1]))]

    def flip(self):
        self.tile = [x[::-1] for x in self.tile]

    # def vertical_flip(self):
    #     self.tile = self.tile[::-1]

    def get_tile_edges(self):
        edges = [self.tile[0], self.tile[-1]]
        edges.append(''.join([r[0] for r in self.tile]))
        edges.append(''.join(r[-1] for r in self.tile))
        return edges

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    # def has_set_neighbors(self):
    #     return sum(1 for x in [self.top, self.bottom, self.left, self.right] is x is not None) == len(self.neighbors)

    def __str__(self):
        return f'{self.id}\n' + '\n'.join(self.tile) + f'neighbors: {self.neighbors}'


camera_tiles = []
for d in data:
    id = int(''.join([x for x in d[0] if x.isdigit()]))
    tile = d[1:]
    camera_tiles.append(CameraTile(id, tile))


for i in range(len(camera_tiles)):
    for j in range(len(camera_tiles)):
        for edge in camera_tiles[i].get_tile_edges():
            if i != j and edge in camera_tiles[j].get_tile_edges() or edge[::-1] in camera_tiles[j].get_tile_edges():
                camera_tiles[i].add_neighbor(camera_tiles[j].id)

camera_tile_map = {x.id: x for x in camera_tiles}
first_tile = [x for x in camera_tile_map.keys()][0]
locked_tiles = [camera_tile_map.pop(first_tile)]
while len(camera_tile_map.keys()) > 0:
    for tile in locked_tiles:
        grid = tile.tile
        tile_left_column = ''.join(r[0] for r in grid)
        tile_right_column = ''.join(r[-1] for r in grid)
        for neighbor_id in tile.neighbors:
            if neighbor_id in camera_tile_map.keys():
                neighbor = camera_tile_map.pop(neighbor_id)
                # top = top
                if grid[0] == neighbor.tile[0]:
                    neighbor.rotate()
                    neighbor.rotate()
                    neighbor.flip()
                    tile.top = neighbor.id
                    neighbor.bottom = tile.id
                # top = bottom
                elif grid[0] == neighbor.tile[-1]:
                    tile.top = neighbor.id
                    neighbor.bottom = tile.id
                # top = top flipped
                elif grid[0] == neighbor.tile[0][::-1]:
                    neighbor.rotate()
                    neighbor.rotate()
                    tile.top = neighbor.id
                    neighbor.bottom = tile.id
                # top = bottom flipped
                elif grid[0] == neighbor.tile[-1][::-1]:
                    neighbor.flip()
                    tile.top = neighbor.id
                    neighbor.bottom = tile.id
                # top = left
                elif grid[0] == ''.join(r[0] for r in neighbor.tile):
                    neighbor.rotate()
                    neighbor.rotate()
                    neighbor.rotate()
                    tile.top = neighbor.id
                    neighbor.bottom = tile.id
                # top = left flipped
                elif grid[0] == ''.join(r[0] for r in neighbor.tile)[::-1]:
                    neighbor.rotate()
                    neighbor.rotate()
                    neighbor.rotate()
                    neighbor.flip()
                    tile.top = neighbor.id
                    neighbor.bottom = tile.id            
                # top = right
                elif grid[0] == ''.join(r[-1] for r in neighbor.tile):
                    neighbor.rotate()
                    neighbor.flip()
                    tile.top = neighbor.id
                    neighbor.bottom = tile.id
                # top = right flipped
                elif grid[0] == ''.join(r[-1] for r in neighbor.tile)[::-1]:
                    neighbor.rotate()
                    tile.top = neighbor.id
                    neighbor.bottom = tile.id
                # bottom = top
                elif grid[-1] == neighbor.tile[0]:
                    tile.bottom = neighbor.id
                    neighbor.top = tile.id
                # bottom = bottom
                elif grid[-1] == neighbor.tile[-1]:
                    neighbor.rotate()
                    neighbor.rotate()
                    neighbor.flip()
                    tile.bottom = neighbor.id
                    neighbor.top = tile.id
                # bottom = top flipped
                elif grid[-1] == neighbor.tile[0][::-1]:
                    neighbor.flip()
                    tile.bottom = neighbor.id
                    neighbor.top = tile.id
                # bottom = bottom flipped
                elif grid[-1] == neighbor.tile[-1][::-1]:
                    neighbor.rotate()
                    neighbor.rotate()
                    tile.bottom = neighbor.id
                    neighbor.top = tile.id
                # bottom = left
                elif grid[-1] == ''.join(r[0] for r in neighbor.tile):
                    neighbor.rotate()
                    neighbor.flip()
                    tile.bottom = neighbor.id
                    neighbor.top = tile.id
                # bottom = left flipped
                elif grid[-1] == ''.join(r[0] for r in neighbor.tile)[::-1]:
                    neighbor.rotate()
                    tile.bottom = neighbor.id
                    neighbor.top = tile.id            
                # bottom = right
                elif grid[-1] == ''.join(r[-1] for r in neighbor.tile):
                    neighbor.rotate()
                    neighbor.rotate()
                    neighbor.rotate()
                    tile.bottom = neighbor.id
                    neighbor.top = tile.id
                # bottom = right flipped
                elif grid[-1] == ''.join(r[-1] for r in neighbor.tile)[::-1]:
                    neighbor.rotate()
                    neighbor.rotate()
                    neighbor.rotate()
                    neighbor.flip()
                    tile.bottom = neighbor.id
                    neighbor.top = tile.id
                # left = top
                elif tile_left_column == neighbor.tile[0]:
                    neighbor.rotate()
                    tile.left = neighbor.id
                    neighbor.right = tile.id
                # left = bottom
                elif tile_left_column == neighbor.tile[-1]:
                    neighbor.rotate()
                    neighbor.flip()
                    neighbor.rotate()
                    neighbor.rotate()
                    # neighbor.vertical_flip()
                    tile.left = neighbor.id
                    neighbor.right = tile.id
                # left = top flipped
                elif tile_left_column == neighbor.tile[0][::-1]:
                    neighbor.rotate()
                    neighbor.vertical_flip()
                    tile.left = neighbor.id
                    neighbor.right = tile.id
                # left = bottom flipped
                elif tile_left_column == neighbor.tile[-1][::-1]:
                    neighbor.rotate()
                    neighbor.rotate()
                    neighbor.rotate()
                    tile.left = neighbor.id
                    neighbor.right = tile.id
                # left = left
                elif tile_left_column == ''.join(r[0] for r in neighbor.tile):
                    neighbor.rotate()
                    neighbor.rotate()
                    neighbor.vertical_flip()
                    tile.left = neighbor.id
                    neighbor.right = tile.id
                # left = left flipped
                elif tile_left_column == ''.join(r[0] for r in neighbor.tile)[::-1]:
                    neighbor.rotate()
                    neighbor.rotate()
                    tile.left = neighbor.id
                    neighbor.right = tile.id            
                # left = right
                elif tile_left_column == ''.join(r[-1] for r in neighbor.tile):
                    tile.left = neighbor.id
                    neighbor.right = tile.id
                # left = right flipped
                elif tile_left_column == ''.join(r[-1] for r in neighbor.tile)[::-1]:
                    neighbor.vertical_flip()
                    tile.left = neighbor.id
                    neighbor.right = tile.id
                # right = top
                elif tile_right_column == neighbor.tile[0]:
                    neighbor.rotate()
                    neighbor.rotate()
                    neighbor.rotate()
                    neighbor.vertical_flip()
                    tile.right = neighbor.id
                    neighbor.left = tile.id
                # right = bottom
                elif tile_right_column == neighbor.tile[-1]:
                    neighbor.rotate()
                    tile.right = neighbor.id
                    neighbor.left = tile.id
                # right = top flipped
                elif tile_right_column == neighbor.tile[0][::-1]:
                    neighbor.rotate()
                    neighbor.vertical_flip()
                    tile.right = neighbor.id
                    neighbor.left = tile.id
                # right = bottom flipped
                elif tile_right_column == neighbor.tile[-1][::-1]:
                    neighbor.rotate()
                    neighbor.rotate()
                    neighbor.rotate()
                    tile.right = neighbor.id
                    neighbor.left = tile.id
                # right = left
                elif tile_right_column == ''.join(r[0] for r in neighbor.tile):
                    tile.right = neighbor.id
                    neighbor.left = tile.id
                # right = left flipped
                elif tile_right_column == ''.join(r[0] for r in neighbor.tile)[::-1]:
                    neighbor.vertical_flip()
                    tile.right = neighbor.id
                    neighbor.left = tile.id            
                # right = right
                elif tile_right_column == ''.join(r[-1] for r in neighbor.tile):
                    neighbor.rotate()
                    neighbor.rotate()
                    neighbor.vertical_flip()
                    tile.right = neighbor.id
                    neighbor.left = tile.id
                # right = right flipped
                elif tile_right_column == ''.join(r[-1] for r in neighbor.tile)[::-1]:
                    neighbor.rotate()
                    neighbor.rotate()
                    tile.right = neighbor.id
                    neighbor.left = tile.id
                locked_tiles.append(neighbor)

                # align neighbor tile
                # locked_tiles.append(neighbor_tile)

for x in locked_tiles:
    if x.point is None:
        x.point = (0, 0)
    if x.top is not None:
        neighbor: CameraTile = [t for t in locked_tiles if t.id == x.top][0]
        if neighbor.point is None:
            neighbor.point = (x.point[0], x.point[1] - 1)
    if x.bottom is not None:
        neighbor: CameraTile = [t for t in locked_tiles if t.id == x.bottom][0]
        if neighbor.point is None:
            neighbor.point = (x.point[0], x.point[1] + 1)
    if x.left is not None:
        neighbor: CameraTile = [t for t in locked_tiles if t.id == x.left][0]
        if neighbor.point is None:
            neighbor.point = (x.point[0] - 1, x.point[1])
    if x.right is not None:
        neighbor: CameraTile = [t for t in locked_tiles if t.id == x.right][0]
        if neighbor.point is None:
            neighbor.point = (x.point[0] + 1, x.point[1])

locked_tiles = sorted(locked_tiles, key=lambda t: (t.point[1], t.point[0]))
# for tile in locked_tiles:
    # tile.tile = [row[1:-1] for row in tile.tile[1:-1]]
grid_size = int(sqrt(len(locked_tiles)))
# for tile in locked_tiles:
    # tile.tile = [row[1:-1] for row in tile.tile[1:-1]]
# TODO: ISSUE IS THIS AND GRID_SIZE
split_tiles = [locked_tiles[i:i + grid_size] for i in range(0, len(locked_tiles), grid_size)]

combined_image = []
for x in split_tiles:
    for row in range(1, len(x[0].tile) - 1):
        line = ''
        for tile in x:
            line += tile.tile[row][1:-1]
        combined_image.append(line)
        print(line)
print('\n')

seamonster_count = 0
seamonster_points = [(1,0), (2,1), (2,4), (1,5), (1,6), (2,7), (2,10), (1,11), (1,12), (2,13), (2,16), (1,17), (0,18), (1,18), (1,19)]
for flip in [False, True]:
    for rotation in range(4):
        for i in range(0, len(combined_image) - 2):
            for j in range(0, len(combined_image[0]) - 19):
                print(f'(i,j={i},{j}) checking for seamonster')
                if all(combined_image[i + dp[0]][j + dp[1]] == '#' for dp in seamonster_points):
                    for dp in seamonster_points:
                        combined_image[i + dp[0]] = combined_image[i + dp[0]][:j + dp[1]] + 'O' + combined_image[i + dp[0]][j + dp[1] + 1:]
                    seamonster_count += 1
        if seamonster_count > 0:
            break
        # print('image after rotation/flip:')
        # for row in combined_image:
            # print(row)
        # print('\n\n')
        # rotate image
        print('Rotating image')
        combined_image = [''.join(x) for x in list(zip(*combined_image[::-1]))]
    if seamonster_count > 0:
        break
    # flip image
    print('Flipping image')
    combined_image = [x[::-1] for x in combined_image]
print(f'Seamonster count: {seamonster_count}')
# total_hashes = sum(row.count('#') for row in combined_image)
# total_os = sum(row.count('O') for row in combined_image)
# seamonster_hashes = len(seamonster_points) * seamonster_count
# print(f'Water roughness: {total_hashes + total_os - seamonster_hashes}') # 1724 = too high : 1499 = too low
final_roughness = sum(row.count('#') for row in combined_image)
print(f'Water roughness: {final_roughness}')

print('Final image:')
for row in combined_image:
    print(row)

    # for x in locked_tiles:
    #     print(x.id)
    #     print(x.tile)
    #     print(f'Top: {x.top}')
    #     print(f'Right: {x.right}')
    #     print(f'Bottom: {x.bottom}')
    #     print(f'Left: {x.left}')
    #     print(f'Point: {x.point}')
    #     print('-------------')
    

# corner_product = 1
# for tile in camera_tiles:
#     if len(tile.neighbors) == 2:
#         print(tile.id)
#         corner_product *= tile.id
# print(corner_product)


# mapped_tiles = []
# re_arranged_tiles = []

# def map_neighbors(tile: CameraTile):
#     # mapped_tiles.append(tile.id)
#     re_arranged_tiles.append(tile.id)
#     # for neighbor_id in tile.neighbors:
#     if len(tile.neighbors) == 0:
#         return
#     neighbor_id = tile.neighbors.pop()
#     neighbor: CameraTile = [x for x in camera_tiles if x.id == neighbor_id][0]
#     # if neighbor.id not in mapped_tiles:
#     grid = tile.tile
#     if neighbor_id in re_arranged_tiles:
#         return

#     # if grid[0] == neighbor[0]:
#         # neighbor.rotate()
#         # neighbor.rotate()
#         # neighbor.flip()
#         # tile.top = neighbor.id
#         # neighbor.bottom = grid.id

#     if tile.top is None:
#         # top = top
#         if grid[0] == neighbor.tile[0]:
#                 neighbor.rotate()
#                 neighbor.rotate()
#                 neighbor.flip()
#                 tile.top = neighbor.id
#                 neighbor.bottom = tile.id
#         # top = bottom
#         elif grid[0] == neighbor.tile[-1]:
#                 tile.top = neighbor.id
#                 neighbor.bottom = tile.id
#         # top = top flipped
#         elif grid[0] == neighbor.tile[0][::-1]:
#                 neighbor.rotate()
#                 neighbor.rotate()
#                 tile.top = neighbor.id
#                 neighbor.bottom = tile.id
#         # top = bottom flipped
#         elif grid[0] == neighbor.tile[-1][::-1]:
#                 neighbor.flip()
#                 tile.top = neighbor.id
#                 neighbor.bottom = tile.id
#         # top = left
#         elif grid[0] == ''.join(r[0] for r in neighbor.tile):
#                 neighbor.rotate()
#                 neighbor.rotate()
#                 neighbor.rotate()
#                 tile.top = neighbor.id
#                 neighbor.bottom = tile.id
#         # top = left flipped
#         elif grid[0] == ''.join(r[0] for r in neighbor.tile)[::-1]:
#                 neighbor.rotate()
#                 neighbor.rotate()
#                 neighbor.rotate()
#                 neighbor.flip()
#                 tile.top = neighbor.id
#                 neighbor.bottom = tile.id            
#         # top = right
#         elif grid[0] == ''.join(r[-1] for r in neighbor.tile):
#             neighbor.rotate()
#             neighbor.flip()
#             tile.top = neighbor.id
#             neighbor.bottom = tile.id
#         # top = right flipped
#         elif grid[0] == ''.join(r[-1] for r in neighbor.tile)[::-1]:
#             neighbor.rotate()
#             tile.top = neighbor.id
#             neighbor.bottom = tile.id
#         # map_neighbors(neighbor)
#     if tile.bottom is None:
#         # bottom = top
#         if grid[-1] == neighbor.tile[0]:
#             tile.bottom = neighbor.id
#             neighbor.top = tile.id
#         # bottom = bottom
#         elif grid[-1] == neighbor.tile[-1]:
#             neighbor.rotate()
#             neighbor.rotate()
#             neighbor.flip()
#             tile.bottom = neighbor.id
#             neighbor.top = tile.id
#         # bottom = top flipped
#         elif grid[-1] == neighbor.tile[0][::-1]:
#             neighbor.flip()
#             tile.bottom = neighbor.id
#             neighbor.top = tile.id
#         # bottom = bottom flipped
#         elif grid[-1] == neighbor.tile[-1][::-1]:
#             neighbor.rotate()
#             neighbor.rotate()
#             tile.bottom = neighbor.id
#             neighbor.top = tile.id
#         # bottom = left
#         elif grid[-1] == ''.join(r[0] for r in neighbor.tile):
#             neighbor.rotate()
#             neighbor.flip()
#             tile.bottom = neighbor.id
#             neighbor.top = tile.id
#         # bottom = left flipped
#         elif grid[-1] == ''.join(r[0] for r in neighbor.tile)[::-1]:
#             neighbor.rotate()
#             tile.bottom = neighbor.id
#             neighbor.top = tile.id            
#         # bottom = right
#         elif grid[-1] == ''.join(r[-1] for r in neighbor.tile):
#             neighbor.rotate()
#             neighbor.rotate()
#             neighbor.rotate()
#             tile.bottom = neighbor.id
#             neighbor.top = tile.id
#         # bottom = right flipped
#         elif grid[-1] == ''.join(r[-1] for r in neighbor.tile)[::-1]:
#             neighbor.rotate()
#             neighbor.rotate()
#             neighbor.rotate()
#             neighbor.flip()
#             tile.bottom = neighbor.id
#             neighbor.top = tile.id
#         # map_neighbors(neighbor)
#     if tile.left is None:
#         tile_left_column = ''.join(r[0] for r in grid)
#         # left = top
#         if tile_left_column == neighbor.tile[0]:
#             neighbor.rotate()
#             tile.left = neighbor.id
#             neighbor.right = tile.id
#         # left = bottom
#         elif tile_left_column == neighbor.tile[-1]:
#             neighbor.rotate()
#             neighbor.rotate()
#             neighbor.rotate()
#             neighbor.vertical_flip()
#             tile.left = neighbor.id
#             neighbor.right = tile.id
#         # left = top flipped
#         elif tile_left_column == neighbor.tile[0][::-1]:
#             neighbor.rotate()
#             neighbor.vertical_flip()
#             tile.left = neighbor.id
#             neighbor.right = tile.id
#         # left = bottom flipped
#         elif tile_left_column == neighbor.tile[-1][::-1]:
#             neighbor.rotate()
#             neighbor.rotate()
#             neighbor.rotate()
#             tile.left = neighbor.id
#             neighbor.right = tile.id
#         # left = left
#         elif tile_left_column == ''.join(r[0] for r in neighbor.tile):
#             neighbor.rotate()
#             neighbor.rotate()
#             neighbor.vertical_flip()
#             tile.left = neighbor.id
#             neighbor.right = tile.id
#         # left = left flipped
#         elif tile_left_column == ''.join(r[0] for r in neighbor.tile)[::-1]:
#             neighbor.rotate()
#             neighbor.rotate()
#             tile.left = neighbor.id
#             neighbor.right = tile.id            
#         # left = right
#         elif tile_left_column == ''.join(r[-1] for r in neighbor.tile):
#             tile.left = neighbor.id
#             neighbor.right = tile.id
#         # left = right flipped
#         elif tile_left_column == ''.join(r[-1] for r in neighbor.tile)[::-1]:
#             neighbor.vertical_flip()
#             tile.left = neighbor.id
#             neighbor.right = tile.id
#         # map_neighbors(neighbor)
#     if tile.right is None:
#         tile_right_column = ''.join(r[-1] for r in grid)
#         # right = top
#         if tile_right_column == neighbor.tile[0]:
#             neighbor.rotate()
#             neighbor.rotate()
#             neighbor.rotate()
#             neighbor.vertical_flip()
#             tile.right = neighbor.id
#             neighbor.left = tile.id
#         # right = bottom
#         elif tile_right_column == neighbor.tile[-1]:
#             neighbor.rotate()
#             tile.right = neighbor.id
#             neighbor.left = tile.id
#         # right = top flipped
#         elif tile_right_column == neighbor.tile[0][::-1]:
#             neighbor.rotate()
#             neighbor.vertical_flip()
#             tile.right = neighbor.id
#             neighbor.left = tile.id
#         # right = bottom flipped
#         elif tile_right_column == neighbor.tile[-1][::-1]:
#             neighbor.rotate()
#             neighbor.rotate()
#             neighbor.rotate()
#             tile.right = neighbor.id
#             neighbor.left = tile.id
#         # right = left
#         elif tile_right_column == ''.join(r[0] for r in neighbor.tile):
#             tile.right = neighbor.id
#             neighbor.left = tile.id
#         # right = left flipped
#         elif tile_right_column == ''.join(r[0] for r in neighbor.tile)[::-1]:
#             neighbor.vertical_flip()
#             tile.right = neighbor.id
#             neighbor.left = tile.id            
#         # right = right
#         elif tile_right_column == ''.join(r[-1] for r in neighbor.tile):
#             neighbor.rotate()
#             neighbor.rotate()
#             neighbor.vertical_flip()
#             tile.right = neighbor.id
#             neighbor.left = tile.id
#         # right = right flipped
#         elif tile_right_column == ''.join(r[-1] for r in neighbor.tile)[::-1]:
#             neighbor.rotate()
#             neighbor.rotate()
#             tile.right = neighbor.id
#             neighbor.left = tile.id
#         map_neighbors(neighbor)
#     re_arranged_tiles.append(neighbor.id)


# # for tile in camera_tiles:
#     # mapped_tiles = []
#     # map_neighbors(tile)
# # mapped_tiles = []
# # for tile in camera_tiles[::-1]:
# #     map_neighbors(tile)

# for x in camera_tiles:
#     print(x.id)
#     print(x.tile)
#     print(f'Top: {x.top}')
#     print(f'Right: {x.right}')
#     print(f'Bottom: {x.bottom}')
#     print(f'Left: {x.left}')
#     print('-------------')

# for x in camera_tiles:
#     print(x.id, ' ', x.neighbors)

# print([f'id: {x.id}: {[_ for _ in x.neighbors]}' for x in camera_tiles])
