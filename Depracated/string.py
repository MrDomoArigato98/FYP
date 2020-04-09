# Import modules
import numpy as np
import cv2
import easygui as gui
import sys
import os
from matplotlib import pyplot as plt
import stdnum.util
from stdnum.eu import banknote
from PIL import Image
import pytesseract

def start_gui():
    #Choices for the GUI buttons,requires an array
    box_choices =["Choose image","Exit Program"]
    user_choice =gui.buttonbox("Insert you banknote image",choices = box_choices)
    if user_choice == "Choose image":   
        try:
			#Call open_image method which returns the image variables
            image  = open_image()
            return(image)
        except:
            sys.exit("Error opening image")
    elif user_choice=="Exit Program":
        sys.exit("User choice to exit, closing")
    
def end_gui(temp_file,serial_number,fake):
	#Concatenate the strings together for the result
    if fake==1:
        end_string= "  and is an invalid serial number"
    else:
        end_string="  and is a valid number"

    program_reply=("The Serial Number is: "+ serial_number + end_string)
	#Box choices in GUI, requires an array
    box_choices =["Main Menu","Exit Program"]
	#Display buttonbox, with image,and choices
    user_choice =gui.buttonbox(program_reply,image = temp_file,choices = box_choices)
	#Remove the image that was written for displaying circles
    os.remove(temp_file)
    
	#Checks which buttons were pressed
    if user_choice =="Main Menu":
        main()
    else:
        sys.exit("Exiting by user choice, closing program")    
    
    
def convert_bgr2rgb(image):
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    return(image)

def convert_bgr2hsv(image):
    image = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    return(image)

def convert_gray(image):
    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    return(image)
    
def open_image():
    f = gui.fileopenbox()
    image = cv2.imread(f)
    return(image)

def median_blur(image):
	image = cv2.medianBlur(image, 9)  
	return(image)

def gaussian_blur(image):
    image = cv2.GaussianBlur(image,(3,3),0)  
    return(image)

def resize(image):
    scale = 60
    width = int(image.shape[1] * scale / 100)
    height = int(image.shape[0] * scale / 100)
    dimensions = (width, height)
    resized = cv2.resize(image, dimensions, interpolation = cv2.INTER_LINEAR_EXACT)
    return(resized)

def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)

def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

def main():
    #temp variables
    fake=0
    temp_file = "temp_image.jpg"
    
    #Getting user input and saving an original copy of it
    image = start_gui()
    original = image
    #Normalizing the image
    normalized = cv2.normalize(image,None,0,255,cv2.NORM_MINMAX)
    #Convert to HSV
    hsv = cv2.cvtColor(normalized, cv2.COLOR_BGR2HSV)
    
    #Array for range for €50 note
    #And bitwise mask
    lower = np.array([0, 0, 13])
    upper = np.array([179, 244, 161])
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(original,original,mask=mask)
    result[mask==0] = (255,255,255)
     
    
    #Top right corner of image for just the serial number
    H,W = result.shape[:2]
    half_x = int(W/2)
    half_y = int(H/2)
    crop_result = result[0:half_y,half_x:W]    
    h,s,v = cv2.split(hsv)
    
    #Temp file for ocr
    cv2.imwrite(temp_file, crop_result) 
    # Include tesseract executable in your path
    pytesseract.pytesseract.tesseract_cmd = r"c:\Program Files\Tesseract-OCR\tesseract.exe"
#    pytesseract.pytesseract.tesseract_cmd = r"D:\Documents\New folder\tesseract.exe"
    
    # Create an image object of PIL library
    image = Image.open(temp_file)
    serial_number = pytesseract.image_to_string(image, lang='eng')
    
    original = convert_bgr2rgb(original)
    plt.subplot(2,2,1)
    plt.imshow(original)
    
    plt.subplot(2,2,2)
    plt.imshow(s)
    
    plt.subplot(2,2,3)
    plt.imshow(result)
    
    plt.subplot(2,2,4)
    plt.imshow(crop_result)
    
    plt.show()
    
    
    try:
        banknote.validate(serial_number)
    except:
        print("Invalid Serial Number") 
        fake=1
        end_gui(temp_file,serial_number,fake)
    
    end_gui(temp_file,serial_number,fake)
    
if __name__ == '__main__':
    main()