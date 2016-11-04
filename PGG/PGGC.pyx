""" cython version of PGG model """

import numpy as np
cimport numpy as np
from libc.stdlib cimport malloc, free
from cpython cimport array
import array

ctypedef np.float DTYPE_t

cdef class PGGC:

    cdef int N
    cdef np.ndarray strategy



    def __init__(self, N):
        self.N = N
        self.strategy = np.random.randint(2, size=self.N)



    cdef void play_c(self, neighbour, neighbour_count, float resource = 1., float enhancement = 1.):

        # pool = [0.]*self.N

        cdef float *pool = <float *>malloc(self.N * sizeof(float))
        cdef float *profit = <float *>malloc(self.N * sizeof(float))
        cdef int idx, nei
        cdef float contrib
        cdef float share

        for idx in xrange(self.N):
            if self.strategy[idx]:  # cooperate
                contrib = resource / neighbour_count[idx]  # contribution to neighbour points
                for nei in neighbour[idx]:
                    pool[nei] += contrib
        for idx in xrange(self.N):
            share = (enhancement * pool[idx]) / neighbour_count[idx]  # share gain from pgg
            for nei in neighbour[idx]:
                profit[nei] += share


        # for idx in xrange(self.N):
        #     self.strategy[idx] = profit[idx]>resource
        # self.strategy = np.array(profit) > resource
        free(pool)
        free(profit)


    def play(self, neighbour, neighbour_count, resource = 1., enhancement = 1.):
        return self.play_c(neighbour, neighbour_count, resource, enhancement)