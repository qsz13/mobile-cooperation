''' PGG model '''
import numpy as np


class PGG:

    def __init__(self, N):
        self.N = N
        self.strategy = np.random.randint(2, size=self.N)  # 1 as c 0 as d

    # def play(self, points, neighbour):


