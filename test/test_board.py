import os
import sys
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.board import Board
import numpy as np

def test(ans, expected, test_name = ''):
    if ans == expected:
        print("Correct -{}- Got: {} and expected: {}".format(test_name, ans, expected))
    else:
        print("Incorrect -{}- Got: {} and expected: {}".format(test_name, ans, expected))
        all_correct = False

def test_takeAction():
    p = Board()
    test(p.validActions(), [i for i in range(p.BOARD_WIDTH)])
    for i in range(p.BOARD_HEIGHT):
        test(p.takeAction(1,2), True)
    test(p.takeAction(1,2), False)
    test(p.validActions(), [i for i in range(p.BOARD_WIDTH) if i != 2])
    for i in range(p.BOARD_HEIGHT):
        test(p.takeAction(-1,3), True)
    test(p.takeAction(-1,3), False)
    test(p.validActions(), [i for i in range(p.BOARD_WIDTH) if i != 2 and i != 3])

def test_check4InARow():
    b = Board()
    test(b.check4InARow(), 0)
    test(b.takeAction(1, 0), True)
    test(b.check4InARow(), 0)
    test(b.takeAction(1, 1), True)
    test(b.check4InARow(), 0)
    test(b.takeAction(1, 2), True)
    test(b.check4InARow(), 0)
    test(b.takeAction(1, 3), True)
    test(b.check4InARow(), 1)
    brd = [[0., 0., 0., 0., 0., 0., 0.],
               [0., 1, 0., 0., 0., 0., 0.],
               [0., 0., 1, 0., 0., 0., 0.],
               [0., 0., 0., 1, 0., 0., 0.],
               [0., 0., 0., 0., 1, 0., 0.],
               [0., 0., 0., 0., 0., 0., 0.]]
    b.board = np.array(brd)
    test(b.check4InARow(), 1)
    brd = [[0., 0., 0., 0., 0., 0., 0.],
               [0., 1, 0., 0., 0., -1., 0.],
               [0., 0., 1, 0., -1., 0., 0.],
               [0., 0., 0., -1, 0., 0., 0.],
               [0., 0., -1., 0., 1, 0., 0.],
               [0., 0., 0., 0., 0., 0., 0.]]
    b.board = np.array(brd)
    test(b.check4InARow(), -1)

test_takeAction()
test_check4InARow()
