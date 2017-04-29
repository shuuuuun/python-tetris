import copy
from constants import *

class Block:
    def __init__(self, id=0, x=0, y=0):
        self.shape = copy.deepcopy(BLOCK_LIST[id]['shape'])
        self.block_id = id
        self.x = x
        self.y = y

    def moveLeft(self):
        self.x -= 1

    def moveRight(self):
        self.x += 1

    def moveDown(self):
        self.y += 1

    def rotate(self):
        newShape = []
        for y in range(NUMBER_OF_BLOCK):
            newShape.append([])
            for x in range(NUMBER_OF_BLOCK):
                newShape[y].append(self.shape[NUMBER_OF_BLOCK - 1 - x][y])
        self.shape = newShape
