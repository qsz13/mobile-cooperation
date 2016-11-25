# cython: profile=True
# cython: linetrace=True
# cython: wraparound=False
# cython: boundscheck=False

""" cython version of PGG model """
import cython
import numpy as np
cimport numpy as np
from libc.stdint cimport uint32_t, uint16_t, uint8_t
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
        cdef uint16_t idx, nei
        cdef np.ndarray[np.float64_t, ndim=1] contrib
        cdef np.ndarray[np.float64_t, ndim=1] share
        cdef np.ndarray[np.uint16_t, ndim=1] neighbour_count
        cdef float probability
        cdef float max_diff
        cdef np.ndarray[np.uint8_t, ndim=1] new_strategy
        neighbour_count = np.sum(self.player,axis=1).astype(np.uint16)
        # print "neighbour_count: "+str(neighbour_count.tolist())
        # print "strategy: "+str(self.strategy.tolist())
        contrib = self.strategy * resource
        contrib /= neighbour_count
        # print "contrib: "+str(contrib.tolist())
        pool = np.dot(contrib, self.player.T)
        # print "pool: "+str(pool.tolist())
        share = enhancement * pool / neighbour_count
        # print "share: "+str(share.tolist())
        profit = np.dot(share, self.player.T)
        profit -= self.strategy*resource
        # print "profit: "+str(profit.tolist())
        # print profit
        # max_diff = self.minmax(profit)
        new_strategy = self.strategy
        # to_c = 0
        # to_d = 0
        for idx in xrange(self.N):
            nei = np.random.choice(np.where(self.player[idx] == True)[0])
            if self.strategy[idx] == self.strategy[nei]:
                continue
            max_diff = self.minmax(profit)

            probability = max(0, (profit[nei]-profit[idx])/max_diff)
            # print probability
            if np.random.rand() < probability:
                new_strategy[idx] = self.strategy[nei]
                # if self.strategy[nei] == 1:
                #     to_c+=1
                # if self.strategy[nei] == 0:
                #     to_d+=1
        # print "to_c "+str(to_c)
        # print "to_d"+str(to_d)

        self.strategy = new_strategy


    def play(self, resource = 1., enhancement = 1.5):
        self.play_c(resource, enhancement)



    def accumulate_neighbour(self,  neighbour):
        self.player = np.logical_or(self.player, neighbour)


    def get_coper_num(self):
        return np.count_nonzero(self.strategy)


    cdef float minmax(self, np.ndarray[np.float64_t, ndim=1] data) :
        return np.max(data)-np.min(data)