import numpy as np

class Board:
    def __init__(self, disp = False):
        self.BOARD_WIDTH = 7
        self.BOARD_HEIGHT = 6
        # [0,0] is bottom left, and BOARD_HEIGHT-1,BOARD_WIDTH-1 is top right
        self.board = np.zeros((self.BOARD_HEIGHT, self.BOARD_WIDTH))
        self.display = disp

    def resetBoard(self):
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
        print("Shouldn't be here -- Take action")
        return False

    def check4InARow(self, debug = False):
        # Check horizontal
        for y in range(self.BOARD_HEIGHT):
            for x in range(self.BOARD_WIDTH - 3):
                arr = self.board[y,x:x+4]
                if np.array_equal(arr, [1,1,1,1]) or np.array_equal(arr, [-1,-1,-1,-1]):
                    if debug:
                        print("Connect 4 - horizontal y = {} x = {}->{}".format(y,x,x+4))
                    return arr[0]
        # Check vertical
        for x in range(self.BOARD_WIDTH):
            for y in range(self.BOARD_HEIGHT - 3):
                arr = self.board[y:y+4,x]
                if np.array_equal(arr, [1,1,1,1]) or np.array_equal(arr, [-1,-1,-1,-1]):
                    if debug:
                        print("Connect 4 - vertical y = {}->{} x = {}".format(y,y+4,x))
                    return arr[0]
        for x in range(self.BOARD_WIDTH-3):
            for y in range(self.BOARD_HEIGHT-3):
                arr = np.array([self.board[y+i,x+i] for i in range(4)])
                if np.array_equal(arr, [1,1,1,1]) or np.array_equal(arr, [-1,-1,-1,-1]):
                    if debug:
                        print("Connect 4 - Diag up y = {}->{} x = {}->{}".format(y,y+4,x, x+4))
                    return arr[0]
        for x in range(self.BOARD_WIDTH-3):
            for y in range(self.BOARD_HEIGHT-1, 2, -1):
                arr = np.array([self.board[y-i,x+i] for i in range(4)])
                if np.array_equal(arr, [1,1,1,1]) or np.array_equal(arr, [-1,-1,-1,-1]):
                    if debug:
                        print("Connect 4 - Diag down y = {}->{} x = {}->{}".format(y,y-4,x, x+4))
                    return arr[0]
        return 0

    def step(self, team, action):
        self.takeAction(team, action)
        result = self.check4InARow()
        done = (result != 0) or (0 not in self.board[-1,:])
        return self.board, result, done
