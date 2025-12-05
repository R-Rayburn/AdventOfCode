from math import sqrt

file_name = 'data.txt'

with open(file_name, 'r') as f:
    data = [x.split('\n') for x in f.read().split('\n\n') if x]


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

    def vertical_flip(self):
        self.tile = self.tile[::-1]

    def get_tile_edges(self):
        edges = [self.tile[0], self.tile[-1]]
        edges.append(''.join([r[0] for r in self.tile]))
        edges.append(''.join(r[-1] for r in self.tile))
        return edges

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

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
                for flip in [False, True]:
                    for rotation in range(4):
                        # top = bottom
                        if grid[0] == neighbor.tile[-1]:
                            tile.top = neighbor.id
                            neighbor.bottom = tile.id
                        # left = right
                        elif tile_left_column == ''.join(r[-1] for r in neighbor.tile):
                            tile.left = neighbor.id
                            neighbor.right = tile.id
                        # right = left
                        elif tile_right_column == ''.join(r[0] for r in neighbor.tile):
                            tile.right = neighbor.id
                            neighbor.left = tile.id
                        # bottom = top
                        elif grid[-1] == neighbor.tile[0]:
                            tile.bottom = neighbor.id
                            neighbor.top = tile.id
                        if (tile.top == neighbor.id or tile.bottom == neighbor.id or
                            tile.left == neighbor.id or tile.right == neighbor.id):
                            locked_tiles.append(neighbor)
                            break
                        neighbor.rotate()
                    if (tile.top == neighbor.id or tile.bottom == neighbor.id or
                        tile.left == neighbor.id or tile.right == neighbor.id):
                        break
                    neighbor.flip()


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
grid_size = int(sqrt(len(locked_tiles)))
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
        print('Rotating image')
        combined_image = [''.join(x) for x in list(zip(*combined_image[::-1]))]
    if seamonster_count > 0:
        break
    # flip image
    print('Flipping image')
    combined_image = [x[::-1] for x in combined_image]
print(f'Seamonster count: {seamonster_count}')
final_roughness = sum(row.count('#') for row in combined_image)
print(f'Water roughness: {final_roughness}')

print('Final image:')
for row in combined_image:
    print(row)

