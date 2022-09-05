import os
import sys
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.viewer import Viewer
import numpy as np

v = Viewer()
brd = np.array([[0., 0., 0., 0., 0., 0., 0.],
                [0., 1., 0., 0., 0., 0., 0.],
                [0., 0., 1., 0., 0., 0., 0.],
                [0., 0., 0., 1., 0., 0., 0.],
                [0., 0., 0., 0., 1., 0., 0.],
                [0., 0., 0., 0., 0., 0., 0.]])
v.displayBoard(brd, pause = 0)
brd = np.array([[1., 0., 0., 0., 0., 0., -1],
                [0., 1., 0., 0., -1, 0., 0.],
                [0., -1, 1., 0., 0., 0., 0.],
                [0., -1, 0., 1., 0., 0., 0.],
                [0., 0., 1., 0., 1., 0., 0.],
                [1., 0., 0., 0., 0., 0., -1]])
v.displayBoard(brd, pause = 0)
