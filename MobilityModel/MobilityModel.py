""" Mobility Model  """

import numpy as np
from pykdtree.kdtree import KDTree
import math
import pyximport

old_get_distutils_extension = pyximport.pyximport.get_distutils_extension
def new_get_distutils_extension(modname, pyxfilename, language_level=None):
    extension_mod, setup_args = old_get_distutils_extension(modname, pyxfilename, language_level)
    extension_mod.language='c++'
    extension_mod.extra_compile_args=["-std=c++11","-O3"]
    return extension_mod,setup_args
pyximport.pyximport.get_distutils_extension = new_get_distutils_extension
pyximport.install(setup_args={'include_dirs': np.get_include()})


from PGG.PGGC import PGGC
# from PGG.pggcpp import PGGCpp

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
        self.pgg = PGGC(N)
        self._init_points()
        self._sigmoid = None
        self._init_sigmoid()

    def _init_sigmoid(self):
        self._sigmoid = np.array([1 / (1 + math.exp(i - 10)) for i in xrange(self.neighbor_limit+1)])


    def _init_points(self):
        u_1 = np.random.uniform(0.0, 1.0, self.N)  # generate n uniformly distributed points
        u_2 = np.random.uniform(0.0, 1.0, self.N)  # generate n uniformly distributed points
        angle = 2*PI*u_2
        radii = self.map.radius * np.sqrt(u_1)
        x = radii * np.cos(angle)
        y = radii * np.sin(angle)
        self.home_pos = np.array((x,y)).T
        # print "init points:"+str(self.home_pos)
        self.cur_pos = self.home_pos
        self.neighbours, self.neighbour_count = self._query_with_pykdtree(self.cur_pos, k=self.neighbor_limit)
        # print "neighbours:" + str(self.neighbours)

    def one_day(self):
        landmark_selection = np.random.randint(len(self.map.landmarks), size=self.N)
        for i in xrange(self.period):
            goto_landmark = np.random.choice([0, 1], self.N, p=[1 - self.lm_possibility, self.lm_possibility])
            # angle = np.zeros(self.N)
            lmc = self.map.landmarks[landmark_selection].T
            # print lmc[0]
            angle = np.arctan2(lmc[1] - self.cur_pos.T[1], lmc[0] - self.cur_pos.T[0])*goto_landmark  # landmark direction
            angle += (2 * np.pi * np.random.uniform(0.0, 1.0))*(1-goto_landmark)    # random direction
            v = self.velocity * self._sigmoid[np.array(self.neighbour_count)]
            x = self.cur_pos.T[0] + v * np.cos(angle)
            y = self.cur_pos.T[1] + v * np.sin(angle)
            self.cur_pos = np.array((x,y)).T
            # print self.cur_pos
        self.neighbours, self.neighbour_count = self._query_with_pykdtree(np.array(self.cur_pos),
                                                                          k=self.neighbor_limit)

        # print self.neighbours
        self.pgg.play(self.neighbours, self.neighbour_count, resource = 1.0, enhancement = 3.0)
        #
        # test = self._query_with_pykdtree(np.array(self.cur_pos+self.map.landmarks))
        # print len(test[5000])
        # self._plot()
        self.cur_pos = self.home_pos
        return self.pgg.get_coper_num()

    def _query_with_pykdtree(self, points, k=30, r=1):
        tree = KDTree(points)
        results, counts = tree.query(points, k=k, distance_upper_bound=r)
        return [r[:counts[idx]] for idx, r in enumerate(results.tolist())], counts
        # return [r for r in results.tolist()], counts


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
