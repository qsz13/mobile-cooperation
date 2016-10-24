#-*- coding:utf-8 -*-
#!/usr/bin/python
import ConfigParser
import time
from ProbabilityModel.hppp import generate_PPP
from ProbabilityModel.rbd import generate_binDecision
from KDTree.kdTree import query_point_r
from KDTree.pyKDTree import pyquery_point_r

_noNode = 5000
_comm_range = 1

if __name__ == "__main__":
    init_policy = generate_binDecision(_noNode)
    x, y, r_circle = generate_PPP(_noNode)
    points = zip(x.ravel(), y.ravel()) # zip the point into tuple (x1, y1) ...
    
    start_time = time.time()
    l_neighbor = query_point_r(points, _comm_range)
    print l_neighbor
    print time.time() - start_time
    
    start_time = time.time()
    l_neighbor = pyquery_point_r(points, _comm_range)
    print l_neighbor
    print time.time() - start_time
    
    #start_time = time.time()
    #neighbor_list = []
    #for i in range(len(x)):
    #    neighbor = kd_tree.query_ball_point([x[i], y[i]], _comm_range)
    #    neighbor_list.append(neighbor)
    #print time.time() - start_time