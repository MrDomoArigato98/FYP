# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 15:21:18 2020

@author: Dominik
"""
import numpy as np
import cv2

def five_note(hsv,original):
    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=5)
    img = cv2.erode(img, kernel, iterations=5)
    img= cv2.normalize(img,None,0,255,cv2.NORM_MINMAX)
   
    cv2.imshow('result', img)
    cv2.waitKey(0)
    return(img)