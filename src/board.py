import numpy as np

from spritesheet import SpriteSheet

class Board:
    def __init__(self, size):
        self.size = size
        self.tile_height = 49
        self.tile_width = 49
        self.board = []
        self.empty_tile = None
        self.puzzle_img = SpriteSheet('../assets/castle_puzzle_solved.bmp')
        self.create_board()
        self.scramble()

    def create_board(self):
        for i in range(self.size ** 2):
            if i == self.size ** 2 - 1:
                self.empty_tile = EmptyTile(i)
                self.empty_tile.x = (self.tile_width + 7) * (i % self.size)
                self.empty_tile.y = (self.tile_height + 7) * int(i / self.size)
                self.board.append(self.empty_tile)
            else:
                tile = Tile(i)
                tile.x = 16 + (self.tile_width + 7) * (i % self.size)
                tile.y = 16 + (self.tile_height + 7) * int(i / self.size)
                tile.image = self.get_tile_image(self.puzzle_img, i)
                self.board.append(tile)

    def get_tile_image(self, image, index):
        img_x = 16 + (self.tile_width + 7) * (index % self.size)
        img_y = 16 + (self.tile_height + 7) * int(index / self.size)
        return image.image_at((img_x, img_y, self.tile_width, self.tile_height))

    def get_current_board(self):
        return np.reshape([x.curr for x in self.board], (self.size, self.size)).tolist()

    def is_solved(self):
        return self.get_current_board() == np.reshape([x.index for x in self.board], (self.size, self.size)).tolist()

    def is_solvable(self, board):
        pass
    
    def move_tile(self, tile):
        self.empty_tile.curr, tile.curr = tile.curr, self.empty_tile.curr
        self.update_board()
        solved = self.is_solved()
        if solved:
            print(solved)

    def on_click(self, event):
        for tile in self.board:
            if type(tile) == Tile and tile.rect.collidepoint(event.pos):
                if self.tile_next_to_empty(tile):
                    self.move_tile(tile)

    def render(self, window):
        for tile in self.board:
            tile.draw(window)

    def scramble(self):
        numbers = np.arange(0, self.size ** 2 - 1)
        perm = np.append(np.random.permutation(numbers), self.size ** 2 - 1).tolist()
        for i, t in enumerate(perm):
            for tile in self.board:
                if tile.index == t:
                    tile.curr = i
        self.update_board()

    def tile_next_to_empty(self, tile):
        return self.empty_tile.curr in (tile.curr + 1, tile.curr - 1, tile.curr + self.size, tile.curr - self.size)

    def update_board(self):
        for tile in self.board:
            tile.x = 16 + (self.tile_width + 7) * (tile.curr % self.size)
            tile.y = 16 + (self.tile_height + 7) * int(tile.curr / self.size)

class Tile:
    def __init__(self, index):
        self.x = None
        self.y = None
        self.image = None
        self.index = index
        self.curr = index
        self.rect = None

    def __str__(self):
        return "x: " + str(self.x) + " y: " + str(self.y)

    def draw(self, window):
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y
        window.blit(self.image, self.rect)


class EmptyTile:
    def __init__(self, index):
        self.x = None
        self.y = None
        self.index = index
        self.curr = index

    def draw(self, window):
        pass