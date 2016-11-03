'''generate Map for mobile'''
import numpy as np

LAMBDA = 1 # the coefficient
PI = np.pi # or put PI = 3.14


class Map:
    _landmark_percentage = 0.001
    landmarks = []

    def _out_of_distance(self, p1, p2, dis):
        return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 > dis ** 2

    def _valid_landmark(self, point, lm_min_dist):
        if self._out_of_distance((0, 0), point, self.radius):
            return False
        for l in self.landmarks:
            if self._out_of_distance(l, point, lm_min_dist):
                return False
        return True

    def _generate_landmark(self, lm_min_dist):
        while len(self.landmarks) < self.landmarks_num:
            lm = self.radius * (2 * np.random.rand(1, 2) - 1)[0]
            if self._valid_landmark(lm, lm_min_dist):
                self.landmarks.append(lm)
        self.landmarks = np.array(self.landmarks)

    def __init__(self, N, lm_min_dist): # Number of points, landmark minimum distance
        n = np.random.poisson(N) * LAMBDA  # size of the circle C
        self.radius = np.sqrt(n / PI)  # radius of the circle C
        self.landmarks_num = N * self._landmark_percentage
        self._generate_landmark(lm_min_dist)


if __name__ == "__main__":
    m = Map(5000, 1)
