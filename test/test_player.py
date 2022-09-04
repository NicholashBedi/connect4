import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.player import Player
from src.viewer import Viewer


def test(ans, expected, test_name = ''):
    if ans == expected:
        print("Correct -{}- Got: {} and expected: {}".format(test_name, ans, expected))
    else:
        print("Incorrect -{}- Got: {} and expected: {}".format(test_name, ans, expected))
        all_correct = False

p = Player()
test(p.validActions(), [i for i in range(p.BOARD_WIDTH)])
for i in range(p.BOARD_HEIGHT):
    test(p.takeAction(1,2), True)
test(p.takeAction(1,2), False)
test(p.validActions(), [i for i in range(p.BOARD_WIDTH) if i != 2])
for i in range(p.BOARD_HEIGHT):
    test(p.takeAction(-1,3), True)
test(p.takeAction(-1,3), False)
test(p.validActions(), [i for i in range(p.BOARD_WIDTH) if i != 2 and i != 3])


v = Viewer()
v.setBoard(p.board)
v.displayBoard()
