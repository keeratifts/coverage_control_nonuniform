#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from astropy.visualization import LogStretch
from astropy.visualization.mpl_normalize import ImageNormalize
from geovoronoi.plotting import plot_voronoi_polys_with_points_in_area, _plot_polygon_collection_with_color
from shapely import geometry
import mpl_scatter_density

class plotting():
    def __init__(self):
        self.fig = plt.figure(figsize=(13,5))
        self.fig.subplots_adjust(wspace=0.3, hspace=0, top=0.9, bottom=0.2)
        self.ax1 = self.fig.add_subplot(121,projection='scatter_density')
        self.ax2 = self.fig.add_subplot(122,projection='scatter_density')
        self.ax1.axis('scaled')
        self.ax2.axis('scaled')
        self.norm = ImageNormalize(vmin=0., vmax=1000, stretch=LogStretch())
        self.major_locator = plt.MultipleLocator(1)
        self.sensor_range = 0.25
        self.sensor_region = []
        self.font = {'size':20}
        self.ax1.set_xlim([0,4])
        self.ax1.set_ylim([0,4])
        self.iteration = 1
        

    def plot_density(self):
        self.ax2.scatter_density(self.x_unit, self.y_unit, cmap='tab20', norm=self.norm, alpha = 0.5)
        self.ax2.set_xlim([0,4])
        self.ax2.set_ylim([0,4])
        self.ax2.xaxis.set_major_locator(self.major_locator)
        self.ax2.yaxis.set_major_locator(self.major_locator)
        self.ax2.set_xlabel('x(m)',self.font, labelpad=10)
        self.ax2.set_ylabel('y(m)',self.font, labelpad=10)
        self.ax2.tick_params(labelsize=18)
    
    def plot_Voronoi(self):
        '''
        All-in-one function to plot Voronoi region polygons `poly_shapes` 
        and the respective points `points` inside a
        geographic area `area_shape` on a matplotlib Axes object `ax`.
        '''
        plot_voronoi_polys_with_points_in_area(self.ax1, self.area_shape, self.poly_shapes, self.coords,
                                               self.poly_to_pt_assignments, points_color='black',
                                               points_markersize=40, voronoi_and_points_cmap=None,
                                               plot_voronoi_opts={'alpha': 0.5})
        self.ax1.scatter(self.coords[:, 0], self.coords[:, 1], color = 'black', s= 30, marker='o', zorder =20)
    
        for centroid in self.new_centroids:
            c1 = centroid
            self.ax1.plot(c1[0],c1[1], 'rs', markersize = 8, zorder = 1)

        self.ax1.set_xlim([0,4])
        self.ax1.set_ylim([0,4])
        self.ax1.xaxis.set_major_locator(self.major_locator)
        self.ax1.yaxis.set_major_locator(self.major_locator)
        self.ax1.set_xlabel('x(m)',self.font, labelpad=10)
        self.ax1.set_ylabel('y(m)',self.font, labelpad=10)
        self.ax1.tick_params(labelsize=18)
        
        self.plot_sensor_range()
        
    def plot_sensor_range(self):
        self.sensor_region = []
        for coord in list(self.coords):
            circ = geometry.Point(coord[0], coord[1]).buffer(self.sensor_range, cap_style=1)
            self.sensor_region.append(circ)
    
        _plot_polygon_collection_with_color(self.ax1, self.sensor_region, color='red', alpha=0.3, zorder=10)
    
    def plot_figure(self, save_fig=False):
        self.plot_Voronoi()
        self.plot_density()
        if save_fig:
            plt.savefig('PNG/FIG_'+str(self.iteration)+'.png')
            self.iteration += 1
        plt.pause(0.001)
        self.ax1.clear()
        self.ax2.clear()