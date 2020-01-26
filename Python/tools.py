#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 19:39:30 2019

@author: VincentMorel
"""

import numpy
import math
from PIL import ImageDraw, Image
import PIL

def find_coeffs(source_coords, target_coords):
    matrix = []
    for s, t in zip(source_coords, target_coords):
        matrix.append([t[0], t[1], 1, 0, 0, 0, -s[0]*t[0], -s[0]*t[1]])
        matrix.append([0, 0, 0, t[0], t[1], 1, -s[1]*t[0], -s[1]*t[1]])
    A = numpy.matrix(matrix, dtype=numpy.float)
    B = numpy.array(source_coords).reshape(8)
    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)

def rotation(angle,image): 
    width,height = image.size
    center = (width,height)
    
    rad = angle*(math.pi/180) 
    
    def points(image):
        width,height = image.size
        x,y = width/2,height/2
        p1 = (-x,y)
        p2 = (x,y)
        p3 = (x,-y)
        p4 = (-x,-y)
        return p1, p2, p3, p4
    
    p1,p2,p3,p4 = points(image)    
    
    def x_prime(pts,rad):
        return int(((pts[0]*math.cos(rad)) - (pts[1]*math.sin(rad))) + center[0] )
    
    def y_prime(pts,rad):
        return int(((pts[0]*math.sin(rad)) + (pts[1]*math.cos(rad))) - center[1])
    
    pt1 = (x_prime(p1,rad),-y_prime(p1,rad))
    pt2 = (x_prime(p2,rad),-y_prime(p2,rad))
    pt3 = (x_prime(p3,rad),-y_prime(p3,rad))
    pt4 = (x_prime(p4,rad),-y_prime(p4,rad))
    return pt1, pt2, pt3, pt4

def rotation2(angle,coord):
    rad = angle*(math.pi/180) 
    
    p1 = (coord[0][0],coord[0][1])
    p2 = (coord[1][0],coord[1][1])
    p3 = (coord[2][0],coord[2][1])
    p4 = (coord[3][0],coord[3][1])
    
    def x_prime(pts,rad):
        return int(((pts[0]*math.cos(rad)) - (pts[1]*math.sin(rad))))
    
    def y_prime(pts,rad):
        return int(((pts[0]*math.sin(rad)) + (pts[1]*math.cos(rad))))
    
    pt1 = [x_prime(p1,rad),y_prime(p1,rad)]
    pt2 = [x_prime(p2,rad),y_prime(p2,rad)]
    pt3 = [x_prime(p3,rad),y_prime(p3,rad)]
    pt4 = [x_prime(p4,rad),y_prime(p4,rad)]
    
    pts_list = [pt1,pt2,pt3,pt4]    
    x_list = [pt1[0],pt2[0],pt3[0],pt4[0]]
    y_list = [pt1[1],pt2[1],pt3[1],pt4[1]]    

    xmin = min(x_list)
    ymin = min(y_list)

    
    if xmin < 0:
        for i in range(4):
            pts_list[i][0] = pts_list[i][0] + (-1 * xmin)
        
    if ymin < 0:
        for i in range(4):
            pts_list[i][1] = pts_list[i][1] + (-1 * ymin) 
        
    
    pt1 = (pts_list[0][0],pts_list[0][1])
    pt2 = (pts_list[1][0],pts_list[1][1])
    pt3 = (pts_list[2][0],pts_list[2][1])
    pt4 = (pts_list[3][0],pts_list[3][1])
    
    return pt1, pt2, pt3, pt4

def pinch(pourcentage,view,image):
    x,y = image.size
    def points2(image):
        p1 = [0,0]
        p2 = [x,0]
        p3 = [x,y]
        p4 = [0,y]
        return p1, p2, p3, p4    
    
    p1,p2,p3,p4 = points2(image)
    
    if view == 0:
        p1[0] = int(p1[0] + (pourcentage * x))
        p2[0] = int(p2[0] - (pourcentage * x))
    
    if view == 1: 
        p2[1] = int(p2[1] + (pourcentage * y))
        p3[1] = int(p3[1] - (pourcentage * y))
    
    if view == 2:
        p3[0] = int(p3[0] - (pourcentage * x))
        p4[0] = int(p4[0] + (pourcentage * x))
        
    if view == 3:
        p4[1] = int(p4[1] - (pourcentage * y))
        p1[1] = int(p1[1] + (pourcentage * y))
        
    return p1,p2,p3,p4


def pinch2(pourcentage,view,coord):

    p1 = [coord[0][0],coord[0][1]]
    p2 = [coord[1][0],coord[1][1]]
    p3 = [coord[2][0],coord[2][1]]
    p4 = [coord[3][0],coord[3][1]]
    
    if view == 0:
        p1[0] = int(p1[0] + (pourcentage * coord[1][0]))
        p2[0] = int(p2[0] - (pourcentage * coord[1][0]))
    
    if view == 1: 
        p2[1] = int(p2[1] + (pourcentage * coord[2][1]))
        p3[1] = int(p3[1] - (pourcentage * coord[2][1]))
    
    if view == 2:
        p3[0] = int(p3[0] - (pourcentage * coord[1][0]))
        p4[0] = int(p4[0] + (pourcentage * coord[1][0]))
        
    if view == 3:
        p4[1] = int(p4[1] - (pourcentage * coord[2][1]))
        p1[1] = int(p1[1] + (pourcentage * coord[2][1]))
        
    pts_list = [p1,p2,p3,p4]    
    x_list = [p1[0],p2[0],p3[0],p4[0]]
    y_list = [p1[1],p2[1],p3[1],p4[1]]    

    xmin = min(x_list)
    ymin = min(y_list)

    
    if xmin < 0:
        for i in range(4):
            pts_list[i][0] = pts_list[i][0] + (-1 * xmin)
        
    if ymin < 0:
        for i in range(4):
            pts_list[i][1] = pts_list[i][1] + (-1 * ymin) 
        
    
    pt1 = (pts_list[0][0],pts_list[0][1])
    pt2 = (pts_list[1][0],pts_list[1][1])
    pt3 = (pts_list[2][0],pts_list[2][1])
    pt4 = (pts_list[3][0],pts_list[3][1])
    
    return pt1, pt2, pt3, pt4   
        
    return p1,p2,p3,p4

def resize(image,ratio):
    w,h = image.size
    
    newsize = ((int(w*ratio),int(h*ratio)))
    image = image.resize(newsize,Image.ANTIALIAS) 
    
    return image

def bounding_box(deg,pts):
    left_candidates = [pts[0][0],pts[3][0]]
    top_candidates = [pts[0][1],pts[1][1]]
    width_candidates = [pts[1][0],pts[2][0]]
    height_candidates = [pts[2][1], pts[3][1]]
    
    left = min(left_candidates)
    top = min(top_candidates)
    width = max(width_candidates) - left
    height = max(height_candidates) - top 
    
#    if deg < 0:
#        top = pts[1][1]
#        left = pts[0][0]
#        width = pts[2][0] - left
#        height = pts[3][1] - top
#    if deg > 0:
#        top = pts[0][1]
#        left = pts[3][0]
#        width = pts[1][0] - left
#        height = pts[2][1] - top
    return top, left, width, height
    