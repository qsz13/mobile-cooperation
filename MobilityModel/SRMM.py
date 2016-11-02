import numpy as np
PI = np.pi

class MobilityModel:

    def _init_points(self, N):
        x = np.zeros(N)  # Cartesian Coordinate x
        y = np.zeros(N)  # Cartesian Coordinate y
        u_1 = np.random.uniform(0.0, 1.0, N)  # generate n uniformly distributed points
        u_2 = np.random.uniform(0.0, 1.0, N)  # generate n uniformly distributed points
        for i in xrange(N):
            angle = 2 * PI * u_2[i]
            radii = self.map.radius * (np.sqrt(u_1[i]))
            x[i] = radii * np.cos(angle)
            y[i] = radii * np.sin(angle)
        self.points = zip(x, y)
        print "init points:"+str(self.points)

    def __init__(self, N, mobile_map):
        self.map = mobile_map
        self._init_points(N)
        self._plot()

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
        plt.scatter(*zip(*self.points))
        plt.scatter(*zip(*self.map.landmarks), color='r')

        plt.show()


