#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from density_func import non_uniform_cvt
from controller import *

if __name__ == '__main__':
    N = 65
    N_POINTS = 8
    outer = [[0.5,0.5], [3,0.5], [3,3], [0.5,3]]
    coords = [[1, 2.5],
    [1.6, 2.5],
    [2.2, 2.5],
    [2.8, 2.5],
    [1, 1.25],
    [1.6, 1.25],
    [2.2, 1.25],
    [2.8, 1.25]]


    cvt = non_uniform_cvt(10000, [1.3,1.3], 0.35, outer, coords)
    #coords = cvt.generate_random(N_POINTS) #generate random coords
    try:
        for j in range(1, N):
            cvt.voronoi_partition(coords)
            cvt.centroid_calculation() #density function
            centroids = cvt.match_pair()
            cvt.plot_figure()
            coords = cvt.cal_tra()
            coords = barrier_certificates(coords, centroids, safety_radius=0.53)
    except:
        pass
