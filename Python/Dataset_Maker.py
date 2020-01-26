#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 20:09:17 2019

@author: VincentMorel
"""

import PIL
from PIL import ImageDraw, Image, ImageFilter
import tools
import numpy as np
import os

# Working directory
path = "/Users/VincentMorel/Desktop/github/Cards_Tracking/Cards"

# list card/background pictures in order to use them. 
# Sometimes, .DS_Store files are created and create errors :
# un-comment 22/24 to fix
background_list = os.listdir(path+"/Backgrounds")
background_list.remove(".DS_Store")
card_list = os.listdir(path+"/Cards")
#card_list.remove(".DS_Store")

with open(path+'/XMLs/Box_points.txt',"a+") as result_file:
    result_file.write("New entry start.. \n")

# Verbose init 
verbose = 1

# Set number of training samples desired
sample_size = 1

# main loop
for n in range(sample_size):
    # Initialize background image and card image from random 
    prob_bkg = [1/len(background_list)]*len(background_list)
    prob_card = [1/len(card_list)]*len(card_list)
    
    multinom_bkg = list(np.random.multinomial(1,prob_bkg))
    draw_bkg = multinom_bkg.index(1)
    bkg_name = background_list[draw_bkg]
    
    multinom_card = list((np.random.multinomial(1,prob_card)))
    draw_card = multinom_card.index(1)
    card_name = card_list[draw_card]
    
    bkg = PIL.Image.open(path+"/Backgrounds/"+bkg_name)
    card = Image.open(path+"/Cards/"+card_name)
    card = card.convert('RGBA')
    
    # Give random size on card image
    ratio = np.random.normal(2.2,0.1)
    print("Card ratio: "+str(round(ratio,2)))
    card = tools.resize(card,ratio)

    # Set a paste position of card around the middle of the background image.
    # Top left corner position is starting coords (0,0), not middle. 
    x_val = bkg.size[0]/2 - card.size[0]/2
    y_val = bkg.size[1]/2 - card.size[1]/2
    
    x_offset = int(np.random.normal(x_val,x_val/5.5))
    y_offset = int(np.random.normal(y_val,y_val/5.5))

    # Copy images
    back_im = bkg.copy()
    card_im = card.copy()
    
    # Set variables to be used in mutation 
    w,h = card_im.size
    a,b,c,d = (0,0), (w,0), (w,h), (0,h)
    coord = [a,b,c,d]
    
    # Set number of mutations for new sample
    mutations = 2
    
    # start mutations loop
    for i in range(mutations):
        # First switch rotation of card, then apply a random perspective
        if i == 0:
            deg = np.random.normal(0.0,4.5)
            d,e,f,g = tools.rotation2(deg,coord)
            print("Rotation Degree = "+str(round(deg,2)))
        if i > 0:
            pourc = np.random.normal(0.04,0.015)
            multi = list(np.random.multinomial(1,(0.25,0.25,0.25,0.25)))
            view = multi.index(1)
            d,e,f,g = tools.pinch2(pourc,view,coord)
            print("Pinch Pourcentage = "+str(round(pourc,4)*100)+", view = "+str(view))
        
        coeffs = tools.find_coeffs(
                coord,
                [d,e,f,g])

        # Transform perspective into a mutation using variables
        card_im = card_im.transform((w*2, h*2), Image.PERSPECTIVE,coeffs,Image.BICUBIC)
        
        # verbose information
        if verbose == 1:
            print(coord)
            print(d,e,f,g)
            card_im.show()
            card_im.save(path+"1.png", quality=100)
            
        # update coord list
        coord = [list(d),list(e),list(f),list(g)]

    # Paste the transformed image into the background 90% of the time 
    # because we want negatives in training sample
    paste_flag = int(np.random.binomial(n=1,p=0.9))
    if paste_flag:
        back_im.paste(card_im,(x_offset, y_offset),card_im)

    # Initialize points list
    pts = coord
    
    # Correct points list using offset
    for i in range(len(pts)): 
        pts[i][0] = (pts[i][0])+x_offset
        pts[i][1] = (pts[i][1])+y_offset
    
        if verbose == 1:
            draw = ImageDraw.Draw(back_im)
            draw.point((pts[i][0],pts[i][1]),fill=(0,0,255))
#    print(pts)
    
    # Random blur application
    rv2 = int(np.random.binomial(n=1,p=0.7))
    if rv2 == 1:
        print("Image blurred")
        back_im = back_im.filter(ImageFilter.BLUR)

    # resize image for faster training 
    resize_ratio = 1/4
    back_im = tools.resize(back_im,resize_ratio)
    
    # adjust list of points
    for i in range(len(pts)): 
        pts[i][0] = int((pts[i][0])*resize_ratio)
        pts[i][1] = int((pts[i][1])*resize_ratio)
        
    print(pts)
    
    # bounding box points
    top, left, width, height = tools.bounding_box(deg,pts)
    
    print(top,left,width,height)
    
    if verbose == 2:
        back_im.show()
    
    # Convert image to Black and White (optional)
#    back_im = back_im.convert("L")
    
    # Save image to sample folder
    back_im.save(path+"/Database/"+str(n)+".jpg", quality=100)
    
    # save image labels to txt
    with open(path+'/XMLs/Box_points.txt',"a+") as result_file:
        result_file.write("\t <image file='"+str(n)+".jpg'> \n")
        if paste_flag == 1:
            result_file.write("\t <box top='"+str(top)+"' left='"+str(left)+"' width='"+str(width)+"' height='"+str(height)+"'> \n")
            result_file.write("\t \t <label>unlabelled</label> \n")
            result_file.write("\t \t <part name='0' x='"+str(pts[0][0])+"' y='"+str(pts[0][1])+"'/> \n")
            result_file.write("\t \t <part name='1' x='"+str(pts[1][0])+"' y='"+str(pts[1][1])+"'/> \n")
            result_file.write("\t \t <part name='2' x='"+str(pts[2][0])+"' y='"+str(pts[2][1])+"'/> \n")
            result_file.write("\t \t <part name='3' x='"+str(pts[3][0])+"' y='"+str(pts[3][1])+"'/> \n")
            result_file.write("\t </box> \n")
        result_file.write("\t </image> \n \n")
    
