import numpy as np
from pykdtree.kdtree import KDTree
import math
PI = np.pi


class MobilityModel:


    def __init__(self, N, mobile_map, lm_possibility, period):
        self.N = N
        self.map = mobile_map
        self.period = period
        self.lm_possibility = lm_possibility
        self.velocity = self.map.radius/period;
        self._init_points()

        # self._plot()

    def _sigmoid(self, x):
        return 1 / (1 + math.exp(-5*x))

    def _init_points(self ):
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
        print "init points:"+str(self.home_pos)
        self.cur_pos = self.home_pos
        self.neighbours = self._query_with_pykdtree(np.array(self.cur_pos))
        print "neighbouts:" + str(self.neighbours)

    def one_day(self):
        landmark_selection = np.random.randint(len(self.map.landmarks), size=self.N)
        for i in xrange(self.period):
            for idx, point in enumerate(self.cur_pos):
                v = self.velocity * self._sigmoid(len(self.neighbours[idx]))
                if np.random.choice([0,1], 1, p=[1-self.lm_possibility, self.lm_possibility])[0]: #goto landmark
                    lm = self.map.landmarks[landmark_selection[idx]]

                    # a =
                else: #random
                    a = 2 * np.pi * np.random.uniform(0.0, 1.0)
                    self.cur_pos[idx] = (point[0] + v * np.cos(a), point[1] + v * np.sin(a))
            self.neighbours = self._query_with_pykdtree(np.array(self.cur_pos))

    def _query_with_pykdtree(self, points, k = 20, r=1):
        tree = KDTree(points)
        neibrs = tree.query(points, k = k, distance_upper_bound = r)[1]
        return [[x for x in nei if x < self.N] for nei in neibrs]


    def _plot(self):
        import matplotlib.pyplot as plt
        r = self.map.radius
        fig = plt.gcf()
        ax = fig.gca()
        plt.xlim(-r, r)
        plt.ylim(-r, r)
        c = plt.Circle((0, 0), radius=r, color='r', linewidth=1, fill=False)
        ax.add_artist(c)
        # plt.plot(x, y, 'bo')
        plt.scatter(*zip(*self.cur_pos))
        plt.scatter(*zip(*self.map.landmarks), color='r')

        plt.show()


