""" cython version of PGG model """

import numpy as np
cimport numpy as np
import random
from libc.stdlib cimport malloc, free
from cpython cimport array
import array

ctypedef np.float DTYPE_t

cdef class PGGC:

    cdef int N
    cdef np.ndarray strategy
    cdef list player


    def __init__(self, N):
        self.N = N
        self.strategy = np.random.randint(2, size=self.N)
        self.player = [[]]*self.N


    cdef void play_c(self, neighbour, neighbour_count, float resource = 1., float enhancement = 1.):

        # pool = [0.]*self.N

        cdef float *pool = <float *>malloc(self.N * sizeof(float))
        cdef float *profit = <float *>malloc(self.N * sizeof(float))
        cdef int idx, nei
        cdef float contrib
        cdef float share

        for idx in xrange(self.N):
            self.player[idx] = list(set(self.player[idx] + neighbour[idx]))

        for idx in xrange(self.N):
            if self.strategy[idx]:  # cooperate
                contrib = resource / neighbour_count[idx]  # contribution to neighbour points
                for nei in self.player[idx]:
                    pool[nei] += contrib
        for idx in xrange(self.N):
            share = (enhancement * pool[idx]) / neighbour_count[idx]  # share gain from pgg
            for nei in self.player[idx]:
                profit[nei] += share


        # for idx in xrange(self.N):
        #     self.strategy[idx] = profit[idx]>resource


        cdef float maxprofit = profit[0]
        cdef float minprofit = profit[0]


        for idx in xrange(self.N):
            if profit[idx] < minprofit:
                minprofit = profit[idx]
            if profit[idx] > maxprofit:
                maxprofit = profit[idx]

        cdef float max_diff = maxprofit - minprofit


        cdef list new_strategy = [0]* self.N
        for idx in xrange(self.N):
            nei = random.choice(self.player[idx])
            if self.strategy[idx] == self.strategy[nei]:
                new_strategy[idx] = self.strategy[nei]
                continue
            nei_pro = profit[nei]
            my_pro = profit[idx]
            probability = max(0, (nei_pro-my_pro)/max_diff)
            if random.random() < probability :
                new_strategy[idx] = self.strategy[nei]
            else:
                new_strategy[idx] = self.strategy[idx]
        self.strategy = np.array(new_strategy)
        free(pool)
        free(profit)


    def play(self, neighbour, neighbour_count, resource = 1., enhancement = 1.):
        return self.play_c(neighbour, neighbour_count, resource, enhancement)

    def get_coper_num(self):
        return sum(self.strategy)
