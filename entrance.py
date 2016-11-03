#-*- coding:utf-8 -*-
#!/usr/bin/python
import ConfigParser
import time
from ProbabilityModel.hppp import generate_PPP
from ProbabilityModel.hppp import cirrdnPJ
from ProbabilityModel.rbd import generate_binDecision
from KDTree.kdTree import query_point_r
from KDTree.pyKDTree import pyquery_point_r
from KDTree.kdTree import query_with_pykdtree
from multiprocessing import Pool

import numpy as np

_noNode = 5000
_comm_range = 1
_move_times = 1000


result_list = []
def log_result(result):
    # This is called whenever foo_pool(i) returns a result.
    # result_list is modified only by the main process, not the pool workers.
    result_list.append(result)

if __name__ == "__main__":

    init_policy = generate_binDecision(_noNode)
    x, y, r_circle = generate_PPP(_noNode)
    # print x, y
    points = zip(x.ravel(), y.ravel()) # zip the point into tuple (x1, y1) ...
    # print points

#ckdtree with 1 job
    # start_time = time.time()
    # for i in range(_move_times):
    #     points = cirrdnPJ(x, y, r_circle)
    #     # print points
    #     l_neighbor = query_point_r(points, _comm_range, 1)
    #     # print l_neighbor
    # print time.time() - start_time

#ckdtree with 4 jobs
    # start_time = time.time()
    # for i in range(_move_times):
    #     points = cirrdnPJ(x, y, r_circle)
    #     # print points
    #     l_neighbor = query_point_r(points, _comm_range, 4)
    #     # print l_neighbor
    # print time.time() - start_time

# pykdtree
    start_time = time.time()
    for i in xrange(_move_times):
        points = cirrdnPJ(x, y, r_circle)
        # print points
        l_neighbor = query_with_pykdtree(points, _comm_range)
        # print l_neighbor
    print time.time() - start_time

#parallel with ckdtree
    # start_time = time.time()
    # locations = [cirrdnPJ(x, y, r_circle) for i in range(_move_times)]
    # pool = Pool(processes=4)
    # result = pool.apply_async(query_point_r, locations)
    # pool.close()
    # pool.join()
    # print time.time() - start_time
    # print result.get(timeout=4)

#Compare query_ball_point with pykdtree
    # points = cirrdnPJ(x, y, r_circle)
    # # print points
    # l_neighbor = query_point_r(points, _comm_range, 4)
    # # print l_neighbor
    # for i in range(0,10):
    #     print l_neighbor[i]
    # l_neighbor = query_with_pykdtree(points, _comm_range)
    # # print l_neighbor
    # for i in range(0,10):
    #     print l_neighbor[1][i]
