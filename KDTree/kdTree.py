from scipy import spatial
from pykdtree.kdtree import KDTree


def query_point_r(points, r=1, n_jobs=8): # list of x, list of y, comm range r
    tree = spatial.cKDTree(points)
    return tree.query_ball_point(points, r, n_jobs=n_jobs)

def query_with_pykdtree(points, r=1): # list of x, list of y, comm range r
    tree = KDTree(points)
    return tree.query(points, k = 50, distance_upper_bound = r)