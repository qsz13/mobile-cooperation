# cython: profile=True
# cython: linetrace=True
# cython: wraparound=False
# cython: boundscheck=False

""" cython version of PGG model """
import cython
import numpy as np
cimport numpy as np
import itertools



cdef class PGGC:

    cdef int N
    cdef np.ndarray strategy
    cdef np.ndarray player

    def __init__(self, N):
        self.N = N
        self.strategy = np.zeros(N, dtype=np.uint8)
        self.strategy[::2] = True
        np.random.shuffle(self.strategy)
        self.player = np.zeros(shape=(self.N, self.N), dtype=np.uint8)


    cdef void play_c(self, np.float32_t resource = 1., np.float32_t enhancement = 1.5):
        cdef np.ndarray[np.float64_t, ndim=1] pool
        cdef np.ndarray[np.float64_t, ndim=1] profit
        cdef int idx, nei
        cdef np.ndarray[np.float64_t, ndim=1] contrib
        cdef np.ndarray[np.float64_t, ndim=1] share
        cdef np.ndarray[np.uint64_t, ndim=1] neighbour_count
        cdef np.float32_t probability
        cdef np.float32_t max_diff
        cdef np.ndarray[np.uint8_t, ndim=1] new_strategy

        neighbour_count = self.player.sum(axis=1).astype(np.uint64)
        contrib = self.strategy * resource
        contrib /= neighbour_count
        pool = np.dot(self.strategy*contrib, self.player)

        share = enhancement * pool / neighbour_count
        profit = np.dot(share, self.player)
        max_diff = self.minmax(profit)

        new_strategy = self.strategy

        for idx in xrange(self.N):
            nei = np.random.choice(np.where(self.player[idx] == True)[0])
            if self.strategy[idx] == self.strategy[nei]:
                continue
            probability = max(0, (profit[nei]-profit[idx])/max_diff)
            if np.random.rand() < probability :
                new_strategy[idx] = self.strategy[nei]
        self.strategy = new_strategy


    def play(self, resource = 1., enhancement = 1.5):
        self.play_c(resource, enhancement)



    def accumulate_neighbour(self,  neighbour):
        self.player = np.logical_or(self.player, neighbour)


    def get_coper_num(self):
        return np.count_nonzero(self.strategy)


    cdef float minmax(self, np.ndarray[np.float64_t, ndim=1] data) :
        return np.max(data)-np.min(data)