""" Mobility Model  """

import numpy as np
from pykdtree.kdtree import KDTree
import math

from PGG.PGG import PGG

PI = np.pi


class MobilityModel:
    def __init__(self, N, mobile_map, lm_possibility, period):
        self.N = N
        self.neighbor_limit = 30
        self.map = mobile_map
        self.period = period
        self.lm_possibility = lm_possibility
        self.velocity = self.map.radius / period
        self.neighbours = []
        self.pgg = PGG(N)
        self._init_points()
        self._sigmoid = []
        self._init_sigmoid()

    def _init_sigmoid(self):
        for i in xrange(self.neighbor_limit+1):
            self._sigmoid.append(1 / (1 + math.exp(i - 10)))

    def _init_points(self):
        x = np.zeros(self.N)  # Cartesian Coordinate x
        y = np.zeros(self.N)  # Cartesian Coordinate y
        u_1 = np.random.uniform(0.0, 1.0, self.N)  # generate n uniformly distributed points
        u_2 = np.random.uniform(0.0, 1.0, self.N)  # generate n uniformly distributed points
        for i in xrange(self.N):
            angle = 2 * PI * u_2[i]
            radii = self.map.radius * (np.sqrt(u_1[i]))
            x[i] = radii * np.cos(angle)
            y[i] = radii * np.sin(angle)
        self.home_pos = zip(x, y)
        # print "init points:"+str(self.home_pos)
        self.cur_pos = self.home_pos
        self.neighbours, self.neighbour_count = self._query_with_pykdtree(np.array(self.cur_pos), k=self.neighbor_limit)
        # print "neighbours:" + str(self.neighbours)

    def one_day(self):
        landmark_selection = np.random.randint(len(self.map.landmarks), size=self.N)
        for i in xrange(self.period):
            goto_landmark = np.random.choice([0, 1], self.N, p=[1 - self.lm_possibility, self.lm_possibility])
            for idx, point in enumerate(self.cur_pos):
                if goto_landmark[idx]:  # goto landmark
                    lm = self.map.landmarks[landmark_selection[idx]]
                    a = np.arctan2(lm[1] - point[1], lm[0] - point[0])
                else:  # random
                    a = 2 * np.pi * np.random.uniform(0.0, 1.0)
                v = self.velocity * self._sigmoid[self.neighbour_count[idx]]
                self.cur_pos[idx] = (point[0] + v * np.cos(a), point[1] + v * np.sin(a))
            self.neighbours, self.neighbour_count = self._query_with_pykdtree(np.array(self.cur_pos),
                                                                              k=self.neighbor_limit)
            # print self.neighbours
            self.pgg.play(self.neighbours, self.neighbour_count, resource = 1, enhancement = 3)
        #
        # test = self._query_with_pykdtree(np.array(self.cur_pos+self.map.landmarks))
        # print len(test[5000])
        # self._plot()
        self.cur_pos = self.home_pos

    def _query_with_pykdtree(self, points, k=30, r=1):
        tree = KDTree(points)
        results, counts = tree.query(points, k=k, distance_upper_bound=r)

        return [[n for n in r if n is not None] for r in results.tolist()], counts
        # return [[x for x in nei if x < self.N] for nei in neibrs]

    def _plot(self):
        import matplotlib.pyplot as plt
        r = self.map.radius
        fig = plt.gcf()
        fig.set_size_inches(7, 7)
        ax = fig.gca()
        plt.xlim(-r, r)
        plt.ylim(-r, r)
        c = plt.Circle((0, 0), radius=r, color='r', linewidth=1, fill=False)
        ax.add_artist(c)
        # plt.plot(x, y, 'bo')
        plt.scatter(*zip(*self.cur_pos))
        plt.scatter(*zip(*self.map.landmarks), color='r')

        plt.show()
