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
        test(p.takeAction(2), True)
    test(p.takeAction(2), False)
    test(p.validActions(), [i for i in range(p.BOARD_WIDTH) if i != 2])
    for i in range(p.BOARD_HEIGHT):
        test(p.takeAction(3), True)
    test(p.takeAction(3), False)
    test(p.validActions(), [i for i in range(p.BOARD_WIDTH) if i != 2 and i != 3])

def test_checkMore4InARow():
    b = Board()
    brd =   [[0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0.]]
    b.board = np.array(brd)
    test(b.check4InARow(), 0)
    brd =   [[0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 1., 0., 0., 0.],
            [0., 0., 0., 0., 1., 0., 0.],
            [0., 0., 0., 0., 0., 1., 0.],
            [0., 0., 0., 0., 0., 0., 1.]]
    b.board = np.array(brd)
    test(b.check4InARow(), 1)


def test_check4InARow():
    b = Board()
    test(b.check4InARow(), 0)
    test(b.takeAction(0), True)
    test(b.takeAction(0), True)
    test(b.check4InARow(), 0)
    test(b.takeAction(1), True)
    test(b.takeAction(1), True)
    test(b.check4InARow(), 0)
    test(b.takeAction(2), True)
    test(b.takeAction(2), True)
    test(b.check4InARow(), 0)
    test(b.takeAction(3), True)
    test(b.check4InARow(), -1)
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

print("test_takeAction")
test_takeAction()
print("test_check4InARow")
test_check4InARow()
print("test_checkMore4InARow")
test_checkMore4InARow()
