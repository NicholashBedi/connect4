import cv2 as cv
import numpy as np
import os
import sys
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from board import Board

class Viewer():
    def __init__(self,b_width = 7, b_height = 6):
        self.BOARD_WIDTH = b_width
        self.BOARD_HEIGHT = b_height
        self.DISK_RADIUS = 30
        self.px_between_disks = 20
        self.WIDTH = self.BOARD_WIDTH*2*self.DISK_RADIUS + (self.BOARD_WIDTH-1)*self.px_between_disks
        self.HEIGHT = self.BOARD_HEIGHT*2*self.DISK_RADIUS + (self.BOARD_HEIGHT-1)*self.px_between_disks
        self.image = np.zeros((self.HEIGHT, self.WIDTH, 3))
        self.board = np.zeros((self.BOARD_HEIGHT, self.BOARD_WIDTH))
        self.setImage()

    def addDisk(self, x, y, team):
        disk_colour = (0,0,0)
        if team == 1:
            disk_colour = (0,255,255)
        elif team == -1:
            disk_colour = (0,0,255)
        cv.circle(self.image,
            (x*(2*self.DISK_RADIUS + self.px_between_disks) + self.DISK_RADIUS,
            self.HEIGHT - (y*(2*self.DISK_RADIUS + self.px_between_disks) + self.DISK_RADIUS)),
            self.DISK_RADIUS, disk_colour, -1)

    def getColourOfTeam(self, team):
        if team == 1:
            return "Yellow"
        if team == -1:
            return "Red"
        return "Invalid input: {}".format(team)

    def setImage(self):
        self.image[:] = (255,0,0)
        for x in range(self.BOARD_WIDTH):
            for y in range(self.BOARD_HEIGHT):
                self.addDisk(x,y, self.board[y,x])

    def setBoard(self, board):
        self.board = board
        self.setImage()

    def displayBoard(self, board, pause = -1):
        self.setBoard(board)
        cv.imshow("Connect4", self.image)
        if pause >= 0:
            cv.waitKey(pause)

    def getMousePress(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDBLCLK:
            self.no_input = False
            self.mouseX = x
            print("Press recived {}".format(self.mouseX // (self.WIDTH//self.BOARD_WIDTH)))

    def getHumanAction(self, board):
        self.setBoard(board)
        cv.imshow("Connect4", self.image)
        cv.setMouseCallback('Connect4', self.getMousePress)
        self.no_input = True
        while self.no_input:
            cv.waitKey(1)
        action = self.mouseX // (self.WIDTH//self.BOARD_WIDTH)
        return action
