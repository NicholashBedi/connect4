import numpy as np
from board import Board
from viewer import Viewer
import cv2 as cv


class agent:
    def __init__(self):
        self.board = Board()
        self.viewer = Viewer()
        self.to_save = True

    def competeRandomAction(self):
        done = False
        team = 1
        self.viewer.displayBoard(self.board.board, pause = False)
        while not done:
            action = np.random.choice(self.board.validActions())
            board, result, done = self.board.step(team, action)
            if done:
                if result != 0:
                    print("Team {} won!".format(
                            self.viewer.getColourOfTeam(result)))
                else:
                    print("Draw".format(result))
            self.viewer.displayBoard(self.board.board, pause = False)
            cv.waitKey(200)
            team *= -1
        self.viewer.displayBoard(self.board.board, pause = True)

if __name__ == "__main__":
    np.random.seed(2)
    a = agent()
    a.competeRandomAction()
