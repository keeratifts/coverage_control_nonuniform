#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 15:12:27 2020

@author: 10969theodore
"""
import imageio


def create_gif(image_list, gif_name, duration=0.35):
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))
    imageio.mimsave(gif_name, frames, 'GIF', duration=duration)
    return


def main():
    image_list = []
    for i in range(1,65):
        image_list.append('/home/robolab/CVT/Voronoi_basic_revised/Voronoi_basic_revised/Nonuniform/PNG/FIG_'+ str(i) + '.png')
    gif_name = 'no_safety.gif'
    duration = 0.1
    create_gif(image_list, gif_name, duration)


if __name__ == '__main__':
    main()

