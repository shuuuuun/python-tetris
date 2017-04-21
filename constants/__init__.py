from .shapeList import SHAPE_LIST

NUMBER_OF_BLOCK = 4

COLS = 12
ROWS = 12

BLOCK_SIZE = 35

HIDDEN_ROWS = NUMBER_OF_BLOCK
LOGICAL_ROWS = ROWS + HIDDEN_ROWS

WIDTH = BLOCK_SIZE * COLS
HEIGHT = BLOCK_SIZE * ROWS
NEXT_WIDTH = BLOCK_SIZE * NUMBER_OF_BLOCK
NEXT_HEIGHT = BLOCK_SIZE * NUMBER_OF_BLOCK

RENDER_INTERVAL = 30
DEFAULT_TICK_INTERVAL = 500
SPEEDUP_RATE = 10

# START_X = Math.floor((COLS - NUMBER_OF_BLOCK) / 2)
START_X = 4
START_Y = 0

BG_COLOR = '#888'

KEYS = {
  37: 'left',  # ←
  39: 'right',  # →
  40: 'down',  # ↓
  38: 'rotate',  # ↑
  32: 'rotate'  # space
}

CLEARLINE_BLOCK = {
  'color': '#aaa',
}

GAMEOVER_BLOCK = {
  'color': '#777',
}

BLOCK_LIST = [
  {
    'color': '#FF6666',
    'shape': SHAPE_LIST[0],
  },
  {
    'color': '#FFCC66',
    'shape': SHAPE_LIST[1],
  },
  {
    'color': '#FFFF66',
    'shape': SHAPE_LIST[2],
  },
  {
    'color': '#CCFF66',
    'shape': SHAPE_LIST[3],
  },
  {
    'color': '#66FF66',
    'shape': SHAPE_LIST[4],
  },
  {
    'color': '#66FFCC',
    'shape': SHAPE_LIST[5],
  },
  {
    'color': '#66FFFF',
    'shape': SHAPE_LIST[6],
  },
]
