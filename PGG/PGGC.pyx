# cython: profile=True
# cython: linetrace=True
""" cython version of PGG model """

import numpy as np
cimport numpy as np
from scipy.sparse import lil_matrix
import random
import itertools

from libcpp.vector cimport vector
from libcpp.unordered_set cimport unordered_set

cdef class PGGC:

    cdef int N
    cdef np.ndarray strategy
    # cdef vector[unordered_set[int]] player
    cdef np.ndarray player
    cdef np.ndarray mtx

    def __init__(self, N):
        self.N = N
        self.strategy = np.random.randint(2, size=self.N)
        # self.player = [[]]*self.N
        self.player = np.zeros(shape=(self.N,self.N), dtype=bool)
        self.mtx = np.zeros(shape=(self.N, self.N), dtype=bool)

    cdef void play_c(self, vector[vector[int]] neighbour, vector[int] neighbour_count, float resource = 1., float enhancement = 1.5):
        # self.player = self.convert_to_matrix(neighbour)

        cdef np.ndarray pool
        cdef np.ndarray profit
        cdef int idx, nei
        cdef np.ndarray contrib
        cdef np.ndarray share
        cdef np.ndarray p = self.convert_to_matrix(neighbour)
        self.player = np.logical_or(self.player, p)
        # for idx in xrange(self.N): # union neighbours
        #     for p in neighbour[idx]:
        #         self.player[idx].insert(p)
            # self.player[idx] = list(set(self.player[idx]+neighbour[idx]))
        neighbour_count = self.player.sum(axis=1)
        contrib = self.strategy * resource / neighbour_count
        pool = np.dot(self.strategy*contrib, self.player)
        share = enhancement * np.array(pool) / neighbour_count
        profit = np.dot(share, self.player)
        # for idx in xrange(self.N):
        #     if self.strategy[idx]:  # cooperate
        #         contrib = resource / len(self.player[idx])  # contribution to neighbour points
        #         for nei in self.player[idx]:
        #             pool[nei] += contrib
        # for idx in xrange(self.N):
        #     share = (enhancement * pool[idx]) / len(self.player[idx])  # share gain from pgg
        #     for nei in self.player[idx]:
        #         profit[nei] += share

        #cdef float max_diff = max(profit) - min(profit)
        minv, maxv = self.minmax(profit)

        cdef float max_diff = maxv - minv
        cdef np.ndarray new_strategy = self.strategy
        # cdef float probability
        for idx in xrange(self.N):
            nei = random.choice(self.player[idx])
            if self.strategy[idx] == self.strategy[nei]:
                continue
            probability = max(0, (profit[nei]-profit[idx])/max_diff)
            if random.random() < probability :
                new_strategy[idx] = self.strategy[nei]
        self.strategy = new_strategy

    def convert_to_matrix(self, vector[vector[int]] neighbour):
        self.mtx.fill(False)
        for row, p in enumerate(neighbour):
            for nei in p:
                self.mtx[row, nei] = True
        return self.mtx

    def play(self, neighbour, neighbour_count, resource = 1., enhancement = 1.5):
        return self.play_c(neighbour, neighbour_count, resource, enhancement)

    def get_coper_num(self):
        return np.count_nonzero(self.strategy)

    def minmax(self, data):
        it = iter(data)
        lo = hi = next(it)
        for x, y in itertools.izip_longest(it, it, fillvalue = lo):
            if x > y:
                x, y = y, x
            if x < lo:
                lo = x
            if y > hi:
                hi = y
        return lo, hi