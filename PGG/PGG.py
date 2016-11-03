''' PGG model '''
import numpy as np



class PGG:

    def __init__(self, N):
        self.N = N
        self.strategy = np.random.randint(2, size=self.N)  # 1 as c 0 as d

    def play(self, neighbour, neighbour_count, resource = 1, enhancement = 1):
        pool = [0]*self.N
        for idx, stgy in enumerate(self.strategy):
            if stgy:
                neibr_num = neighbour_count[idx]
                contrib = float(resource)/neibr_num
                for i in xrange(neibr_num):
                    pool[neighbour[idx][i]] += contrib
        profit = [0]*self.N
        for idx, stgy in enumerate(pool):
            neibr_num = neighbour_count[idx]
            for i in xrange(neibr_num):
                profit[neighbour[idx][i]] += (enhancement*pool[idx])/neibr_num

        for idx, p in enumerate(profit):
            if p > resource:
                self.strategy[idx] = 1
            else:
                self.strategy[idx] = 0

        # print profit


