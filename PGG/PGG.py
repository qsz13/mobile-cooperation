''' PGG model '''
import numpy as np
import random


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



class PGGMtx:

    def __init__(self, N):
        self.N = N
        self.strategy = np.random.randint(2, size=self.N)  # 1 as c 0 as d
        self.player = np.zeros(shape=(self.N,self.N), dtype=bool)
        # self.temp = [[]]*self.N

    def play(self, neighbour, resource = 1., enhancement = 1.):

        # for idx in xrange(self.N):
        #     self.temp[idx] = list(set(neighbour[idx]+self.temp[idx]))
        # pool = [0.]*self.N
        # profit = [0.]*self.N
        # for idx in xrange(self.N):
        #     if self.strategy[idx]:  # cooperate
        #         contrib = resource / len(self.temp[idx])  # contribution to neighbour points
        #         for i in self.temp[idx]:
        #             pool[i] += contrib
        # # print pool
        # # print self.strategy
        # for idx in xrange(self.N):
        #     share = (enhancement * pool[idx]) / len(self.temp[idx])  # share gain from pgg
        #     for i in self.temp[idx]:
        #         profit[i] += share
        #
        # print profit


        # self.player = np.logical_or(self.player, self.convert_to_matrix(neighbour))
        self.convert_to_matrix(neighbour)
        neighbour_count = self.player.sum(axis=1)
        contrib = self.strategy * resource / neighbour_count
        pool = np.dot(self.strategy*contrib, self.player)
        share = enhancement * pool / neighbour_count
        profit = np.dot(share, self.player)

        max_diff = max(profit) - min(profit)
        new_strategy = self.strategy
        r = np.random.rand(self.N)
        for idx in xrange(self.N):
            nei = random.choice(np.where(self.player[idx] == True)[0])
            if self.strategy[idx] == self.strategy[nei]:
                continue
            probability = max(0, (profit[nei] - profit[idx]) / max_diff)
            if r[idx] < probability:
                new_strategy[idx] = self.strategy[nei]
        self.strategy = new_strategy

    def convert_to_matrix(self, neighbour):
        # mtx = np.zeros(shape=(self.N, self.N), dtype=bool)
        for row, p in enumerate(neighbour):
            for nei in p:
                self.player[row, nei] = True
        # return mtx

    def get_coper_num(self):
        return sum(self.strategy)