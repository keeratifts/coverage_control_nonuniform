#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from shapely import geometry
from geovoronoi import coords_to_points, points_to_coords, voronoi_regions_from_coords
import numpy as np
import math
from scipy.integrate import odeint
import random

class voronoi():
    def __init__(self, outer, coords):
        self.area_shape = geometry.Polygon(outer)
        self.coords = coords
        self.old_centroids = (np.zeros((len(self.coords), 2)))
    
    def generate_random(self, number):
        self.coords = []
        minx, miny, maxx, maxy = self.area_shape.bounds
        while len(self.coords) < number:
            pnt = geometry.Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
            if self.area_shape.contains(pnt):
                self.coords.append(pnt)
        self.coords = points_to_coords(self.coords)
        return self.coords
    
    def update_coords(self, coords):
        self.pts = [p for p in coords_to_points(coords) if p.within(self.area_shape)]
        self.coords = points_to_coords(self.pts)

    
    def voronoi_partition(self, coords):
        self.update_coords(coords)
        self.poly_shapes, self.pts, self.poly_to_pt_assignments = voronoi_regions_from_coords(self.coords, self.area_shape, accept_n_coord_duplicates= 0)
    
    def cal_tra(self):
        T=2
        t=np.linspace(0,T,num=300)
        omega = math.pi*2/T
        point_lists = []
        for i in range(len(self.coords)):
            y_list_x = [self.coords[i][0],0,0,0,0,0,0,0,0,0,0]
            y_list_y = [self.coords[i][1],0,0,0,0,0,0,0,0,0,0]
            result_x = odeint(self.diff_equation, y_list_x, t, args=(self.coords[i][0]-self.new_centroids[i][0], omega, self.new_centroids[i][0] - self.old_centroids[i][0]))
            result_y = odeint(self.diff_equation, y_list_y, t, args=(self.coords[i][1]-self.new_centroids[i][1], omega, self.new_centroids[i][1] - self.old_centroids[i][1]))
            result_xt = result_x[:,0]
            result_yt = result_y[:,0]
            new_result = np.vstack((np.array(result_xt), np.array(result_yt))).T
            point_lists.append(list(new_result))

        for i in range(len(self.coords)):
            self.coords[i] = point_lists[i][1]

        self.old_centroids = self.new_centroids
        return self.coords
    
    def diff_equation(self, y_list, t, e, omega, c_dot):
        ki = 200
        sum_fu = 0
        coe = 0
        for i in range(1,len(y_list)):
            if i%2 == 0:
                coe = int(i/2)
                sum_fu += (y_list[i] + e*math.cos(coe*omega*t)) * math.cos(coe*omega*t)
            else:
                coe = int((i+1)/2)
                sum_fu += (y_list[i] + e*math.sin(coe*omega*t)) * math.sin(coe*omega*t)
        result = []
        result.append(-ki*e-sum_fu + 20*math.sin(math.pi*t))
        for i in range(1,len(y_list)):
            if i%2 == 0:
                coe = int(i/2)
                result.append((-e)*coe*e*omega*math.cos(coe*omega*t) + (ki*e+c_dot) *math.sin(coe*omega*t))
            else:
                coe = int((i+1)/2)
                result.append(e*coe*omega*math.sin(coe*omega*t) + (ki*e+c_dot) *math.cos(coe*omega*t))
        return np.array(result)



