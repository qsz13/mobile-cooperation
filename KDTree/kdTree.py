from scipy import spatial

def query_point_r(points, r): # list of x, list of y, comm range r
    neighbor_list = []
    # points = zip(x.ravel(), y.ravel()) # zip the point into tuple (x1, y1) ...
    tree = spatial.KDTree(points)
    neighbor = tree.query_ball_point(points, r)
    neighbor_list.append(neighbor)
    return neighbor_list