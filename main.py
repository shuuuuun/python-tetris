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

def drawBoard(win):
    box = win.subwin(BOARD_LINES * BASE_BLOCK_LINES, BOARD_COLS * BASE_BLOCK_COLS, 0, 0)
    box.box()
    box.refresh()

def drawBox(win, x=0, y=0):
    box = win.subwin(BASE_BLOCK_LINES, BASE_BLOCK_COLS, y * BASE_BLOCK_LINES, x * BASE_BLOCK_COLS)
    # box.border()
    box.box()
    box.refresh()

def drawBlock(win, boardX, boardY, id):
    # shape = SHAPE_LIST[id]
    block = BLOCK_LIST[id]
    # blockId = block['id'];
    for y in range(NUMBER_OF_BLOCK):
        for x in range(NUMBER_OF_BLOCK):
            if not block['shape'][y][x]:
                continue
            drawX = x + boardX
            drawY = y + boardY
            drawBox(win, drawX, drawY)

@wrapper
def main(stdscr):
    stdscr.clear()
    # stdscr.erase()

    # stdscr.box(1, 1)
    # box = curses.newwin(12, 12)
    # box = stdscr.subwin(12, 12, 0, 0)
    # box.border()
    # box.box()
    # box.refresh()
    # box.getkey()
    drawBoard(stdscr)
    # drawBox(stdscr, 0, 0)
    
    # sample block
    # for i in range(0, 12):
    #     drawBox(stdscr, i, i)

    drawBlock(stdscr, 3, 0, 0)

    # for i in range(0, 11):
    #     v = i-10
    #     if v != 0:
    #         stdscr.addstr(i, 0, '10 divided by {} is {}'.format(v, 10/v))
    #     # time.sleep(0.1)
    #     # stdscr.refresh()

    # stdscr.move(10, 10)
    stdscr.refresh()
    stdscr.getkey()
