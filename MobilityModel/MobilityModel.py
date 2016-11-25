""" Mobility Model  """
import numpy as np
from pykdtree.kdtree import KDTree
import math
import pyximport
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

MonoFont = FontProperties('monospace')

old_get_distutils_extension = pyximport.pyximport.get_distutils_extension
def new_get_distutils_extension(modname, pyxfilename, language_level=None):
    extension_mod, setup_args = old_get_distutils_extension(modname, pyxfilename, language_level)
    extension_mod.language='c'
    extension_mod.extra_compile_args=["-march=native","-O3","-ffast-math"]
    return extension_mod,setup_args
pyximport.pyximport.get_distutils_extension = new_get_distutils_extension
pyximport.install(setup_args={'include_dirs': np.get_include()})

from PGG.PGGC import PGGC

PI = np.pi

class MobilityModel:
    def __init__(self, N, mobile_map, nb_limit, lm_possibility, period, enhance, drawed):
        self.N = N
        self.map = mobile_map
        self.neighbor_limit = nb_limit
        self.lm_possibility = lm_possibility
        self.period = period
        self.enhancement = enhance
        self.velocity = self.map.radius / period
        self.pgg = PGGC(N)
        self._init_points()
        self._sigmoid = None
        self._init_sigmoid()
        landmark_selection = np.random.randint(len(self.map.landmarks), size=self.N)
        self.lmc = self.map.landmarks[landmark_selection].T
        self.plotted = drawed

    def _init_sigmoid(self):
        self._sigmoid = np.array([1 / (1 + math.exp(i - 15)) for i in xrange(self.neighbor_limit+1)])

    def _init_points(self):
        angle = 2*PI*np.random.uniform(0.0, 1.0, self.N)
        radii = self.map.radius * np.sqrt(np.random.uniform(0.0, 1.0, self.N))
        x = np.float32(radii * np.cos(angle))
        y = np.float32(radii * np.sin(angle))
        self.home_pos = np.array((x,y))
        self.cur_pos = self.home_pos
        self._query_with_pykdtree(self.cur_pos.T, k=self.neighbor_limit)

    def _get_angle(self):

        goto_landmark = np.random.choice([0, 1], self.N, p=[1 - self.lm_possibility, self.lm_possibility])
        angle = np.arctan2(self.lmc[1] - self.cur_pos[1],
                           self.lmc[0] - self.cur_pos[0]) * goto_landmark  # landmark direction
        angle += (2 * np.pi * np.random.uniform(0.0, 1.0, self.N)) * (1 - goto_landmark)  # random direction
        return angle

    def _calculate_cur_pos(self, angle):
        v = self.velocity * self._sigmoid[np.array(self.neighbour_count)]
        x = np.float32(self.cur_pos[0] + v * np.cos(angle))
        y = np.float32(self.cur_pos[1] + v * np.sin(angle))
        self.cur_pos = np.array((x, y))

    def one_day(self, day):
        if day % 1 == 0:
            print "clear:" + str(day)
            self.pgg.clear_player()
        for i in xrange(self.period):

            landmark_selection = np.random.randint(len(self.map.landmarks), size=self.N)
            self.lmc = self.map.landmarks[landmark_selection].T
            angle = self._get_angle()
            self._calculate_cur_pos(angle)

            # print id(self.cur_pos)
            # self.cur_pos[0] += v * np.cos(angle)
            # self.cur_pos[1] += v * np.sin(angle)
            # print id(self.cur_pos)


            nei = self._query_with_pykdtree(self.cur_pos.T, k=self.neighbor_limit)
            self.pgg.accumulate_neighbour(nei)

            if not self.plotted:
                 self._plot_map(i)
                 if i == self.period - 1:
                     self.plotted = True
                     plt.close()

        self.pgg.play(resource = 1.0, enhancement = self.enhancement)
        self.cur_pos = self.home_pos
        return self.pgg.get_coper_num()/float(self.N)

    def _query_with_pykdtree(self, points, k = 20, r = np.float32(1.)):
        tree = KDTree(points)
        results, self.neighbour_count = tree.query(points, k = k, distance_upper_bound = r)
        return results


    def _plot_map(self, idx):
        r = self.map.radius + 6
        #fig, ax = plt.subplots()
        fig = plt.gcf()
        ax = fig.gca()

        fig.set_size_inches(7.5, 7.5)

        plt.xlim(-r, r)
        plt.ylim(-r, r)
        c = plt.Circle((0, 0), radius = self.map.radius, color = 'r', linewidth = 0.5, fill = False)
        ax.add_artist(c)
        # plt.plot(x, y, 'bo')
        node = plt.scatter(*zip(*self.cur_pos), s = 0.2, color = 'b')
        landmark = plt.scatter(*zip(*self.map.landmarks), color = 'r')
        ax.set_title(u'Distribution Map of %i Nodes in Daily Step %i\n' % (self.N, idx), fontproperties = MonoFont, fontsize = 18)
        fontP = FontProperties()
        fontP.set_family('sans-serif')
        fontP.set_size(12)
        ax.legend((node, landmark), (u'Node', u'Landmark'), prop = fontP)
        #plt.axes().set_aspect('equal', 'datalim')
        fig.savefig(u'output/map_distribution_%iNode_%iLmk_%i.png' % (self.N, len(self.map.landmarks), idx), dpi = 300)
        plt.clf()