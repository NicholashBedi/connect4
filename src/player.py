import numpy as np

class Player:
    def __init__(self):
        self.BOARD_WIDTH = 7
        self.BOARD_HEIGHT = 6
        # [0,0] is bottom left, and BOARD_HEIGHT-1,BOARD_WIDTH-1 is top right
        self.board = np.zeros((self.BOARD_HEIGHT, self.BOARD_WIDTH))

    def validActions(self):
        return [i for i in range(self.BOARD_WIDTH) if self.isActionValid(i)]

    def isActionValid(self, action):
        if action < 0 or action >= self.BOARD_WIDTH:
            return False
        return self.board[-1,action] == 0

    def takeAction(self, team, action):
        if self.board[-1,action] != 0 :
            return False
        for i in range(self.BOARD_HEIGHT):
            if self.board[i,action] == 0:
                self.board[i,action] = team
                return True
        print("Shouldn't be here")
        return False
