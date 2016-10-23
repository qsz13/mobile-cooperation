from scipy import spatial

def query_point_r(points, r): # list of x, list of y, comm range r
    tree = spatial.cKDTree(points)
    return tree.query_ball_point(points, r)