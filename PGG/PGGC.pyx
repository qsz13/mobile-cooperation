# cython: profile=True
# cython: linetrace=True
# cython: wraparound=False
# cython: boundscheck=False
""" cython version of PGG model """
import numpy as np
cimport numpy as np

ctypedef np.uint8_t DTYPE_uint8_t
ctypedef np.float_t DTYPE_float_t

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


    cdef void play_c(self, float resource = 1., double enhancement = 1.5):
        cdef np.ndarray pool
        cdef np.ndarray profit
        cdef int idx, nei
        cdef np.ndarray contrib
        # cdef np.ndarray share
        cdef np.ndarray neighbour_count
        neighbour_count = self.player.sum(axis=1)
        contrib = self.strategy * resource
        contrib /= neighbour_count
        pool = np.dot(self.strategy*contrib, self.player)
        pool *= enhancement
        pool /= neighbour_count
        profit = np.dot(pool, self.player)
        cdef float max_diff = self.minmax(profit)
        cdef np.ndarray new_strategy = self.strategy
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

    # cdef accumulate_neighbour_c(self, np.ndarray neighbour):
    #     cdef int i,j
    #     for i in xrange(self.N):
    #         for j in xrange(self.N):
    #             if neighbour[i][j] == 1 :
    #                 self.player[i][j] = 1

    def accumulate_neighbour(self,  neighbour):
        # self.accumulate_neighbour_c(neighbour)
        # print neighbour.dtype
        # print id(self.player)
        # self.player|=neighbour

        self.player = np.logical_or(self.player, neighbour)
        # print id(self.player)


    def get_coper_num(self):
        return np.count_nonzero(self.strategy)


    cdef float minmax(self, np.ndarray data) :
        return np.max(data)-np.min(data)