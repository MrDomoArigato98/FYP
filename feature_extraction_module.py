# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 18:56:22 2020

@author: Dominik
"""
import cv2
import os
from matplotlib import pyplot as plt
import main as cvmod

def percentage(found, total):
    if (found == 0):
        print("No matches found")
        return(0)
    else:
        return (100 * float(found)/float(total))

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images

def cropPercentage(result):
    try:
        #Get height and width through getting shape of image
        H,W = result.shape[:2]
        
        print(H,W)
        #Next we get 10% of the top left portion of the image
        H = H/2
        W = W/4
        print(H,W)
        
        #Crop to use only the 10%
        crop_result = result[0:int(H),0:int(W)]
        return(crop_result)
    except:
        print("Could not crop result, returning original image")
        return(result)

def clahe(image):
    try:
        
        clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(4,4))
        contrasted = clahe.apply(image)
        contrasted=cv2.bilateralFilter(contrasted, 9, 75, 75)
        return(contrasted)
    except:
        print("Error CLAHE in feature extraction module")
        return(image)

def feature_extract(test_image,folder):
    
    original_images = load_images_from_folder(folder)

    #Convert all images to gray for feature extraction
    original_1_gray = cvmod.convert_gray(original_images[0])
    original_2_gray = cvmod.convert_gray(original_images[1])
    test_gray = cvmod.convert_gray(test_image)
    
    #Resize all images to same size
    test_gray       = cvmod.resize(test_gray)
    original_1_gray = cvmod.resize(original_1_gray)
    original_2_gray = cvmod.resize(original_2_gray)
    
    #Use only 10% of each image
    original_1_gray = cropPercentage(original_1_gray)
    original_2_gray = cropPercentage(original_2_gray)
    test_gray       = cropPercentage(test_gray)
    
    #Contrast Limited Adaptive Histogram Equalization
    original_1_gray = clahe(original_1_gray)
    original_2_gray = clahe(original_2_gray)
    test_gray       = clahe(test_gray)
    
    # cv2.imshow("test", test_gray)
    # cv2.imshow("test1", original_1_gray)
    cv2.waitKey(0)
    
    orb = cv2.ORB_create(nfeatures=500)
   
    original_1_kp, original_1_desc = orb.detectAndCompute(original_1_gray, None)
    original_2_kp, original_2_desc = orb.detectAndCompute(original_2_gray, None)
    input_kp, input_desc = orb.detectAndCompute(test_gray, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)
    
    matches1 = bf.match(original_1_desc, input_desc)
    matches2 = bf.match(original_2_desc, input_desc)
    #short distance matches
    matches1 = sorted(matches1, key = lambda x : x.distance)
    matches2 = sorted(matches2, key = lambda x : x.distance)
    
    result = cv2.drawMatches(original_1_gray, original_1_kp, test_gray, input_kp, matches1, test_gray, flags = 2)
    
    # Display the best matching points
    plt.rcParams['figure.figsize'] = [14.0, 7.0]
    plt.title('Best Matching Points')
    plt.imshow(result)
    plt.show()


    average = len(matches1) + len(matches2)
    average=average/2
    
    print("\nNumber of Matching Keypoints - Original 1 and Test image ", len(matches1))
    print("\nNumber of Matching Keypoints - Original 2 and Test image ", len(matches2))
    
    print("Authenticity Percentage = " + str(percentage(average, len(original_1_kp)))+"%")
    
    threshold =  str(percentage(average, len(original_1_kp)))
    
    return(threshold)
    
