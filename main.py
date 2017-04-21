import sys
from tetris import Tetris

try:
    Tetris()
except KeyboardInterrupt:
    print('KeyboardInterrupt')
    sys.exit()
