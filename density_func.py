#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from shapely import geometry
from plotting import plotting
from geovoronoi import coords_to_points
from voronoi import voronoi


class non_uniform_cvt(voronoi, plotting):
    def __init__(self, numbers, target, deviation, outer, coords, **kwargs):
        '''
        :param int numbers: how many 'point' in the plot
        :param list target: (x, y) the position of the density function
        :param float deviation: how far the spread, the standard deviation
        :param list outer: the boundery of shape
        :param list coords: the positions of the agents
        '''

        plotting.__init__(self) 
        super(non_uniform_cvt, self).__init__(outer, coords, **kwargs)
        self.x_unit = np.random.normal(target[0], deviation, numbers)
        self.y_unit = np.random.normal(target[1], deviation, numbers)
    

    def value_contribution(self):
        '''
        x_unit and y_unit is output 10000
        '''
        point_value = np.vstack((np.array(self.x_unit), np.array(self.y_unit))).T  # rearrange into (x coordinate, y coordinate) like a 10000 output value
        poly_nums = len(self.poly_shapes) # poly_nums = 8 
        region_value =[[] for i in range(poly_nums)] # region_value = [[], [], [], [], [], [], [], []] depend on how many agent
        for i, p in enumerate(point_value):
            for j, poly in enumerate(self.poly_shapes):
                point = geometry.Point(p) # turn x_unit and y_unit into Point
                if point.within(poly): # turn x_unit and y_unit (Point form) is within poly_shapes
                    region_value[j].append(p) # put turn x_unit and y_unit (Point form) into region_value[j]
                    
        return np.array(region_value, dtype=object)
    
    
    def centroid_calculation(self):
        '''
        for the right plot density function, among the 10000 numbers, in the middle there is a centroid
        '''
        region_value = self.value_contribution()
        sum_value = []
        for i in range(len(self.poly_shapes)):
            init = [0,0]
            for j in region_value[i]:
                init += j
            sum_value.append(init)
        self.poly_centroids = []
        for i in range(len(self.poly_shapes)):
            poly_size = len(region_value[i])
            if poly_size == 0:
                # self.poly_centroids.append([0,0])
                ori_centroid = [p.centroid.coords[0] for p in self.poly_shapes]
                self.poly_centroids.append(list(ori_centroid[i]))
            else:
                poly_dense_x = sum_value[i][0]/poly_size
                poly_dense_y = sum_value[i][1]/poly_size
                self.poly_centroids.append([poly_dense_x,poly_dense_y])
        for i in range(len(self.x_unit)):
            self.x_unit[i] += 0.02
            self.y_unit[i] += 0.02
        return self.poly_centroids
        

    def match_pair(self):
        '''
        assign correct centroid for each points
        '''
        self.new_centroids = []
        self.poly_centroids = list(self.poly_centroids)
        points = coords_to_points(list(self.coords)) # Convert a NumPy array of 2D coordinates `coords` to a list of shapely Point objects, and also uses shapely points for same format
        for i, p in enumerate(points): # element in new_coords # you can get index, element thur enumerate()
            for j, poly in enumerate(self.poly_shapes): # go thur each shapely points # enumerate() to get element instead of index
                if p.within(poly): # if new_coords(shapely point form) in poly_shapes / if new_coords is found inside of poly_shapes
                    # new_centroids[j] picks out the array list and put into pair
                    pair = self.poly_centroids[j] 
                    # each poly_centroids that in poly_shapes, each to pair
                    self.new_centroids.append(pair)

        return self.new_centroids