from pykdtree.kdtree import KDTree

def pyquery_point_r(points, r): # list of x, list of y, comm range r
    tree = KDTree(points)
    return tree.query_ball_point(points, r)