# cython: profile=True
# cython: linetrace=True
""" cython version of PGG model """
import cython
import numpy as np
cimport numpy as np
import itertools

ctypedef np.uint8_t DTYPE_uint8_t
ctypedef np.float_t DTYPE_float_t

cdef class PGGC:

    cdef int N
    cdef np.ndarray strategy
    cdef np.ndarray player
    cdef np.ndarray mtx

    def __init__(self, N):
        self.N = N
        self.strategy = np.zeros(N, dtype=np.uint8)
        self.strategy[::2] = True
        np.random.shuffle(self.strategy)
        self.player = np.zeros(shape=(self.N, self.N), dtype=np.uint8)
        self.mtx = np.zeros(shape=(self.N, self.N), dtype=np.uint8)

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cdef void play_c(self, float resource = 1., double enhancement = 1.5):
        cdef np.ndarray pool
        cdef np.ndarray profit
        cdef int idx, nei
        cdef np.ndarray contrib
        cdef np.ndarray share
        # self.player = np.logical_or(self.player, neighbour)

        neighbour_count = self.player.sum(axis=1)
        contrib = self.strategy * resource / neighbour_count
        pool = np.dot(self.strategy*contrib, self.player)
        share = enhancement * np.array(pool) / neighbour_count
        profit = np.dot(share, self.player)
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

    # @cython.boundscheck(False)
    # @cython.wraparound(False)
    # cdef accumulate_neighbour_c(self, DTYPE_uint8_t[:,:] neighbour):
    #     self.player = np.logical_or(self.player, neighbour)


    def accumulate_neighbour(self, neighbour):
        self.player = np.logical_or(self.player, neighbour)

        # self.accumulate_neighbour_c(neighbour)

    def get_coper_num(self):
        return np.count_nonzero(self.strategy)

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cdef float minmax(self, np.ndarray data) :

        return np.max(data)-np.min(data)
        # it = iter(data)
        # lo = hi = next(it)
        # for x, y in itertools.izip_longest(it, it, fillvalue = lo):
        #     if x > y:
        #         x, y = y, x
        #     if x < lo:
        #         lo = x
        #     if y > hi:
        #         hi = y
        # return hi - lo