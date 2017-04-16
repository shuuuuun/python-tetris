# import sys, time
import time
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

    def tick(self, stdscr):
        # stdscr.addstr('hoge', 1)
        # time.sleep(0.1)
        time.sleep(DEFAULT_TICK_INTERVAL)
        self.tick(stdscr)

    def main(self, stdscr):
        stdscr.clear()

        self.drawBoard(stdscr)
        # self.drawBox(stdscr, 0, 0)
        
        self.drawBlock(stdscr, 3, 0, 0)
        # self.tick(stdscr)

        # stdscr.move(10, 10)
        stdscr.refresh()
        # stdscr.getkey()
        # stdscr.getkey('w')
        while True:
            # c = stdscr.getch()
            c = stdscr.getkey()
            print(c)
            # if c == ord('q'):
            if c == 'q':
                break
