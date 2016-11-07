# cython: profile=True
# cython: linetrace=True
""" cython version of PGG model """

import numpy as np
cimport numpy as np
from scipy.sparse import lil_matrix
import random

from libcpp.vector cimport vector
from libcpp.unordered_set cimport unordered_set

cdef class PGGC:

    cdef int N
    cdef vector[int] strategy
    cdef vector[unordered_set[int]] player
    # cdef public np.matrix player

    def __init__(self, N):
        self.N = N
        self.strategy = np.random.randint(2, size=self.N)
        self.player = [[]]*self.N



    cdef void play_c(self, vector[vector[int]] neighbour, vector[int] neighbour_count, float resource = 1., float enhancement = 1.):
        # self.player = self.convert_to_matrix(neighbour)

        cdef vector[float] pool = [0.]*self.N
        cdef vector[float] profit = [0.]*self.N
        cdef int idx, nei
        cdef float contrib
        cdef float share
        # p = self.convert_to_matrix(neighbour)
        # self.player = np.logical_or(self.player, p)
        for idx in xrange(self.N): # union neighbours
            for p in neighbour[idx]:
                self.player[idx].insert(p)
            # self.player[idx] = list(set(self.player[idx]+neighbour[idx]))

        for idx in xrange(self.N):
            if self.strategy[idx]:  # cooperate
                contrib = resource / len(self.player[idx])  # contribution to neighbour points
                for nei in self.player[idx]:
                    pool[nei] += contrib
        for idx in xrange(self.N):
            share = (enhancement * pool[idx]) / len(self.player[idx])  # share gain from pgg
            for nei in self.player[idx]:
                profit[nei] += share

        cdef float max_diff = max(profit) - min(profit)

        cdef vector[int] new_strategy = self.strategy
        cdef float probability
        for idx in xrange(self.N):
            nei = random.choice(list(self.player[idx]))
            if self.strategy[idx] == self.strategy[nei]:
                continue
            probability = max(0, (profit[nei]-profit[idx])/max_diff)
            if random.random() < probability :
                new_strategy[idx] = self.strategy[nei]
        self.strategy = new_strategy

    def convert_to_matrix(self, vector[vector[int]] neighbour):
        mtx = np.zeros(shape=(self.N,self.N), dtype=bool)
        # print type(mtx)
        for row,p in enumerate(neighbour):
            for col,nei in enumerate(p):
                mtx[row, col] = True
        return mtx
        # print mtx.todense()



    def play(self, neighbour, neighbour_count, resource = 1., enhancement = 1.):
        return self.play_c(neighbour, neighbour_count, resource, enhancement)

    def get_coper_num(self):
        return sum(self.strategy)
