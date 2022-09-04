import cv2 as cv
import numpy as np

class Viewer():
    def __init__(self):
        self.DISK_HEIGHT = 6
        self.DISK_WIDTH = 7
        self.DISK_RADIUS = 30
        self.px_between_disks = 20
        self.WIDTH = self.DISK_WIDTH*2*self.DISK_RADIUS + (self.DISK_WIDTH-1)*self.px_between_disks
        self.HEIGHT = self.DISK_HEIGHT*2*self.DISK_RADIUS + (self.DISK_HEIGHT-1)*self.px_between_disks
        self.image = np.zeros((self.HEIGHT, self.WIDTH, 3))
        self.board = np.zeros((self.HEIGHT, self.WIDTH))
        self.setImage()

    def addDisk(self, x, y):
        disk_colour = (0,0,0)
        if self.board[y,x] == 1:
            disk_colour = (0,255,255)
        elif self.board[y,x] == -1:
            disk_colour = (0,0,255)
        cv.circle(self.image,
            (x*(2*self.DISK_RADIUS + self.px_between_disks) + self.DISK_RADIUS,
            self.HEIGHT - (y*(2*self.DISK_RADIUS + self.px_between_disks) + self.DISK_RADIUS)),
            self.DISK_RADIUS, disk_colour, -1)

    def setImage(self):
        self.image[:] = (255,0,0)
        for x in range(self.DISK_WIDTH):
            for y in range(self.DISK_HEIGHT):
                self.addDisk(x,y)

    def setBoard(self, board):
        self.board = board.copy()
        self.setImage()

    def displayBoard(self):
        cv.imshow("Connect4", self.image)
        cv.waitKey(0)

if __name__ == "__main__":
    v = Viewer()
    v.board[1,1] = 1
    v.board[0,1] = -1
    v.board[5,6] = -1
    v.board[2,5] = 1
    v.setImage()
    v.displayBoard()
