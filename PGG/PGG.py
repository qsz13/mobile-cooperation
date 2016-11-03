''' PGG model '''
import numpy as np



class PGG:

    def __init__(self, N):
        self.N = N
        self.strategy = np.random.randint(2, size=self.N)  # 1 as c 0 as d

    def play(self, neighbour, neighbour_count, resource = 1, enhancement = 1):
        pool = [0]*self.N
        for idx, stgy in enumerate(self.strategy):
            if stgy:  # cooperate
                contrib = float(resource)/neighbour_count[idx]  # contribution to neighbour points
                # for nei in neighbour[idx]:
                for i in xrange(neighbour_count[idx]):
                    pool[neighbour[idx][i]] += contrib
        profit = [0]*self.N
        for idx, stgy in enumerate(pool):
            share = (enhancement * pool[idx]) / neighbour_count[idx]  # share gain from pgg
            for i in xrange(neighbour_count[idx]):
                profit[neighbour[idx][i]] += share

        for idx, p in enumerate(profit):
            if p > resource:
                self.strategy[idx] = 1
            else:
                self.strategy[idx] = 0



