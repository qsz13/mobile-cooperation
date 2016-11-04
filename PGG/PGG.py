''' PGG model '''
import numpy as np



class PGG:

    def __init__(self, N):
        self.N = N
        self.strategy = np.random.randint(2, size=self.N)  # 1 as c 0 as d

    def play(self, neighbour, neighbour_count, resource = 1., enhancement = 1.):
        resource = float(resource)
        enhancement = float(enhancement)



        pool = [0.]*self.N
        profit = [0.]*self.N
        for idx in xrange(self.N):
            if self.strategy[idx]:  # cooperate
                contrib = resource / neighbour_count[idx]  # contribution to neighbour points
                for i in neighbour[idx]:
                    pool[i] += contrib
        for idx in xrange(self.N):
            share = (enhancement * pool[idx]) / neighbour_count[idx]  # share gain from pgg
            for i in neighbour[idx]:
                profit[i] += share


        # pool = [0.] * self.N
        # profit = [0.] * self.N
        #
        # contrib = (self.strategy * float(resource) / neighbour_count).tolist()
        #
        # for idx in xrange(self.N):
        #     if self.strategy[idx]:  # cooperate
        #         for i in neighbour[idx]:
        #             pool[i] += contrib[idx]
        # share = (enhancement * np.array(pool) / neighbour_count).tolist()
        #
        # for idx in xrange(self.N):
        #     for i in neighbour[idx]:
        #         profit[i] += share[idx]

        self.strategy = np.array(profit) > resource



