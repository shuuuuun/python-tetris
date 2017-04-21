import copy
import random
import curses
from threading import Timer
from constants import *

BOARD_LINES = ROWS
BOARD_COLS = COLS

BASE_BLOCK_LINES = 2
BASE_BLOCK_COLS = 3


class Tetris:
    def __init__(self):
        curses.wrapper(self.main)

    def drawBorder(self, win):
        box = win.subwin(BOARD_LINES * BASE_BLOCK_LINES, BOARD_COLS * BASE_BLOCK_COLS, 0, 0)
        box.box()
        box.refresh()

    def drawBox(self, win, x=0, y=0):
        box = win.subwin(BASE_BLOCK_LINES, BASE_BLOCK_COLS, y * BASE_BLOCK_LINES, x * BASE_BLOCK_COLS)
        # box.border()
        box.box()
        box.refresh()

    def drawBoard(self, win):
        for y in range(ROWS):
            for x in range(COLS):
                boardX = x
                boardY = y + HIDDEN_ROWS
                if not self.board[boardY][boardX]:
                    continue
                self.drawBox(win, x, y)

    def drawBlock(self, win, block):
        for y in range(NUMBER_OF_BLOCK):
            for x in range(NUMBER_OF_BLOCK):
                if not block['shape'][y][x]:
                    continue
                drawX = x + block['x']
                drawY = y + block['y'] - HIDDEN_ROWS
                if drawY >= 0:
                    self.drawBox(win, drawX, drawY)

    def drawCurrentBlock(self, win):
        self.drawBlock(win, self.currentBlock)

    def render(self, stdscr):
        stdscr.clear()
        self.drawBorder(stdscr)
        self.drawBoard(stdscr)
        self.drawCurrentBlock(stdscr)
        # stdscr.addstr(0, 0, 'hogehoge')
        stdscr.refresh()

    def main(self, stdscr):
        self.newGame(stdscr)

        while True:
            c = stdscr.getch()
            if c == ord('q'):
                self.quitGame()
                # raise KeyboardInterrupt
                break
            elif c == curses.KEY_LEFT:
                self.moveBlockLeft()
            elif c == curses.KEY_RIGHT:
                self.moveBlockRight()
            elif c == curses.KEY_DOWN:
                self.moveBlockDown()
            elif c == curses.KEY_UP:
                self.rotateBlock()

    def newGame(self, stdscr):
        self.initGame()
        self.startGame(stdscr)

    def initGame(self):
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
        if not self.moveBlockDown():
            self.freeze()
            self.clearLines()
            if self.checkGameOver():
                self.quitGame()
                return False
            self.frameCount += 1
            self.createCurrentBlock()
            self.createNextBlock()

        if self.isPlayng:
            self.render(stdscr)
            self.timer = Timer(self.tickInterval / 1000, self.tick, [stdscr])
            self.timer.start()

    def quitGame(self):
        self.isPlayng = False
        self.timer.cancel()

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
        # shape = blockConst['shape']
        block = copy.deepcopy(blockConst)
        block.update({
            'id': id,
            # 'shape': [],
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
        id = random.randint(0, len(BLOCK_LIST) - 1)
        self.nextBlock = self.createBlock(id)

    def freeze(self):
        for y in range(NUMBER_OF_BLOCK):
            for x in range(NUMBER_OF_BLOCK):
                boardX = x + self.currentBlock['x']
                boardY = y + self.currentBlock['y']
                if not self.currentBlock['shape'][y][x] or boardY < 0:
                    continue
                self.board[boardY][boardX] = self.currentBlock['id'] + 1 if self.currentBlock['shape'][y][x] else 0

    def clearLines(self):
        clearLineLength = 0 # 同時消去ライン数
        filledRowList = []

        for y in reversed(range(LOGICAL_ROWS)):
            isRowFilled = self.board[y].count(0) == 0
            if not isRowFilled:
                continue
            filledRowList.append(y)
            clearLineLength += 1
            self.sumOfClearLines += 1
            self.tickInterval -= SPEEDUP_RATE # 1行消去で速度を上げる

        if len(filledRowList) > 0:
            for row in reversed(filledRowList):
                del self.board[row]
                self.board.insert(0, BLANK_ROW)

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
        rotatedBlock = copy.deepcopy(self.currentBlock)
        rotatedBlock['shape'] = self.rotate(self.currentBlock['shape'])
        isValid = self.validate(0, 0, rotatedBlock)
        if isValid:
            self.currentBlock = rotatedBlock
        return isValid

    def rotate(self, shape):
        shape = shape or self.currentBlock['shape']
        newBlockShape = []
        for y in range(NUMBER_OF_BLOCK):
            newBlockShape.append([])
            for x in range(NUMBER_OF_BLOCK):
                newBlockShape[y].append(shape[NUMBER_OF_BLOCK - 1 - x][y])
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
                isOutsideBoard = boardY >= len(self.board) or boardX >= len(self.board[boardY])
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
