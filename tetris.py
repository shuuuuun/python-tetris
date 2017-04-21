# import sys, time
import time
import copy
import curses
from curses import wrapper
# import constants
# import constants.index
# from constants import *
from constants.index import *
# from constants.shapeList import SHAPE_LIST

BOARD_LINES = 12
BOARD_COLS = 12

BASE_BLOCK_LINES = 2
BASE_BLOCK_COLS = 3

# print(NUMBER_OF_BLOCK)


class Tetris:
    # def __new__(cls):
    def __init__(self):
        wrapper(self.main)

    def drawBoard(self, win):
        box = win.subwin(BOARD_LINES * BASE_BLOCK_LINES, BOARD_COLS * BASE_BLOCK_COLS, 0, 0)
        box.box()
        box.refresh()

    def drawBox(self, win, x=0, y=0):
        box = win.subwin(BASE_BLOCK_LINES, BASE_BLOCK_COLS, y * BASE_BLOCK_LINES, x * BASE_BLOCK_COLS)
        # box.border()
        box.box()
        box.refresh()

    def drawBlock(self, win, boardX, boardY, id):
        # shape = SHAPE_LIST[id]
        block = BLOCK_LIST[id]
        # blockId = block['id'];
        for y in range(NUMBER_OF_BLOCK):
            for x in range(NUMBER_OF_BLOCK):
                if not block['shape'][y][x]:
                    continue
                drawX = x + boardX
                drawY = y + boardY
                self.drawBox(win, drawX, drawY)

    def drawCurrentBlock(self, win):
        boardX = self.currentBlock['x']
        boardY = self.currentBlock['y']
        # print(boardX, boardY)
        # blockId = self.currentBlock['id']
        # print(blockId)
        # self.drawBlock(win, boardX, boardY, blockId)
        self.drawBlock(win, boardX, boardY, 0)
        # if not (this.currentBlock.shape and this.currentBlock.shape.length):
        #   return
        # for y in range(NUMBER_OF_BLOCK):
        #   for x in range(NUMBER_OF_BLOCK):
        #     blockId = self.currentBlock.id
        #     if (!self.currentBlock.shape[y][x] || isNaN(blockId) || blockId < 0):
        #         continue
        #     drawX = x + self.currentBlock['x']
        #     drawY = y + self.currentBlock['y'] - HIDDEN_ROWS
        #     self.drawBlock(drawX, drawY, blockId)

    def render(self, stdscr):
        stdscr.clear()
        self.drawBoard(stdscr)
        self.drawCurrentBlock(stdscr)
        stdscr.refresh()

    def main(self, stdscr):
        stdscr.clear()

        self.drawBoard(stdscr)
        # self.drawBox(stdscr, 0, 0)
        
        # self.drawBlock(stdscr, 3, 0, 0)
        # self.tick(stdscr)
        self.newGame(stdscr)

        # stdscr.move(10, 10)
        stdscr.refresh()
        # stdscr.getkey()
        # stdscr.getkey('w')
        while True:
            # c = stdscr.getch()
            c = stdscr.getkey()
            # print(c)
            # if c == ord('q'):
            if c == 'q':
                self.isPlayng = False
                break
            elif c == 'KEY_LEFT':
                self.moveBlockLeft()
            elif c == 'KEY_RIGHT':
                self.moveBlockRight()
            elif c == 'KEY_DOWN':
                self.moveBlockDown()
            elif c == 'KEY_UP':
                self.rotateBlock()

    def newGame(self, stdscr):
        self.initGame()
        self.startGame(stdscr)

    def initGame(self):
        # clearTimeout(self.tickId)
        # self.stopRender()
        self.isPlayng = False
        self.lose = False
        self.tickInterval = DEFAULT_TICK_INTERVAL
        self.sumOfClearLines = 0
        self.score = 0
        self.frameCount = 0
        self.initBoard()
        self.initBlock()
        self.createNextBlock()
        # self.render()

    def startGame(self, stdscr):
        self.isPlayng = True
        self.createCurrentBlock()
        self.createNextBlock()
        # self.startRender()
        self.tick(stdscr)

    def tick(self, stdscr):
        # clearTimeout(self.tickId)
        if not self.moveBlockDown():
          self.freeze()
          self.clearLines()
          if self.checkGameOver():
            self.quitGame()
            return False
          self.frameCount += 1
          self.createCurrentBlock()
          self.createNextBlock()
        # self.tickId = setTimeout(() => self.tick(), self.tickInterval);

        if self.isPlayng:
            self.render(stdscr)
            time.sleep(self.tickInterval / 1000)
            self.tick(stdscr)

    def quitGame(self):
        self.isPlayng = False

    # def pauseGame(self):
    #     # clearTimeout(self.tickId)
    #     # self.stopRender()

    def resumeGame(self):
        if not self.isPlayng:
            return
        # self.tickId = setTimeout(() => self.tick(), self.tickInterval)
        # self.startRender()

    def initBoard(self):
        self.board = []
        for y in range(LOGICAL_ROWS):
          self.board.insert(y, [])
          for x in range(COLS):
            # self.board[y][x] = 0
            self.board[y].insert(x, 0)

    def initBlock(self):
        self.nextBlock = self.createBlock(0)
        self.currentBlock = self.createBlock(0)
        self.currentBlock['x'] = START_X
        self.currentBlock['y'] = START_Y

    def createBlock(self, id = 0):
        blockConst = BLOCK_LIST[id] or {}
        shape = blockConst['shape']
        block = copy.deepcopy(blockConst)
        block.update({
            'shape': [],
            'x': 0,
            'y': 0,
        })
        # for y in range(NUMBER_OF_BLOCK):
        #     block['shape'].insert(y, [])
        #     for x in range(NUMBER_OF_BLOCK):
        #         block['shape'][y][x] = shape[y][x] or 0
        return block

    def createCurrentBlock(self):
        if not self.nextBlock:
            self.createNextBlock()
        self.currentBlock = self.nextBlock
        self.currentBlock['x'] = START_X
        self.currentBlock['y'] = START_Y

    def createNextBlock(self):
        # id = Math.floor(Math.random() * BLOCK_LIST.length)
        # self.nextBlock = self.createBlock(id)
        self.nextBlock = self.createBlock(0)

    def freeze(self):
        for y in range(NUMBER_OF_BLOCK):
          for x in range(NUMBER_OF_BLOCK):
            boardX = x + self.currentBlock['x']
            boardY = y + self.currentBlock['y']
            if not self.currentBlock.shape[y][x] or boardY < 0:
                continue
            self.board[boardY][boardX] = self.currentBlock.id + 1 if self.currentBlock.shape[y][x] else 0

    def clearLines(self):
        clearLineLength = 0 # 同時消去ライン数
        filledRowList = []

        # for ( y = LOGICAL_ROWS - 1; y >= 0; --y ) {
        #   isRowFilled = self.board[y].every((val) => val !== 0)
        #   if not isRowFilled:
        #       continue
        #   filledRowList.push(y)
        #   clearLineLength++
        #   self.sumOfClearLines++
        #   self.tickInterval -= SPEEDUP_RATE # 1行消去で速度を上げる

        # if filledRowList.length:
        #     filledRowList.reverse().forEach((row) => {
        #       self.board.splice(row, 1)
        #       self.board.unshift(BLANK_ROW)
        #     })

        # calc score
        # self.score += (clearLineLength <= 1) ? clearLineLength : Math.pow(2, clearLineLength)

    def moveBlockLeft(self):
        isValid = self.validate(-1, 0)
        if isValid:
          self.currentBlock['x'] -= 1
        return isValid

    def moveBlockRight(self):
        isValid = self.validate(1, 0)
        if isValid:
          self.currentBlock['x'] += 1
        return isValid

    def moveBlockDown(self):
        isValid = self.validate(0, 1)
        if isValid:
          self.currentBlock['y'] += 1
        return isValid

    def rotateBlock(self):
        rotatedBlock = Object.assign({}, self.currentBlock)
        rotatedBlock.shape = self.rotate(self.currentBlock.shape)
        isValid = self.validate(0, 0, rotatedBlock)
        if isValid:
          self.currentBlock = rotatedBlock
        return isValid

    def rotate(self, shape):
        shape = shape or self.currentBlock.shape
        newBlockShape = []
        for y in range(NUMBER_OF_BLOCK):
          newBlockShape[y] = []
          for x in range(NUMBER_OF_BLOCK):
            newBlockShape[y][x] = shape[NUMBER_OF_BLOCK - 1 - x][y]
        return newBlockShape;

    def rotateBoard(self, sign):
        newBoard = []
        for y in range(ROWS):
          newBoard[y] = []
          for x in range(COLS):
            newBoard[y][x] = self.board[COLS - 1 - x + HIDDEN_ROWS][y]
        for i in range(HIDDEN_ROWS):
          newBoard.unshift(BLANK_ROW)
        self.board = newBoard
        return newBoard

    def validate(self, offsetX = 0, offsetY = 0, block = None):
        block = block or self.currentBlock
        nextX = block['x'] + offsetX
        nextY = block['y'] + offsetY

        for y in range(NUMBER_OF_BLOCK):
          for x in range(NUMBER_OF_BLOCK):
            if not (block['shape'] and block['shape'][y][x]):
              continue
            boardX = x + nextX
            boardY = y + nextY
            isOutsideLeftWall = boardX < 0
            isOutsideRightWall = boardX >= COLS
            isUnderBottom = boardY >= LOGICAL_ROWS
            isOutsideBoard = self.board[boardY] is None or self.board[boardY][boardX] is None 
            isExistsBlock = (not isOutsideBoard) and self.board[boardY][boardX]
            if isOutsideLeftWall or isOutsideRightWall or isUnderBottom or isOutsideBoard or isExistsBlock:
              return False
        return True

    def checkGameOver(self):
        # ブロックの全てが画面外ならゲームオーバー
        isGameOver = True
        for y in range(NUMBER_OF_BLOCK):
          for x in range(NUMBER_OF_BLOCK):
            boardX = x + self.currentBlock['x']
            boardY = y + self.currentBlock['y']
            if boardY >= HIDDEN_ROWS:
              isGameOver = False
              break
        return isGameOver
