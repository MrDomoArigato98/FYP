# Import modules
import cv2
from matplotlib import pyplot as plt
import stdnum.util
from datetime import datetime
from stdnum.eu import banknote
from PIL import Image
import pytesseract
import sys
import os
import numpy as np
import easygui as gui
#My own modules
import database_module as dbmod
import gui_module as guimod
import feature_extraction_module as fem

temp_file = "temp_image.jpg" # Used for OCR
temp_file_gui = "temp_imag1.jpg"
serial_number="t"
real_note = True
value = 0

def text_extract(image,folder):
        try:
            #Original untouched
            image = resize(image)

            #Crop the Original image
            croppedImage = crop_right_corner(image)

            clahe_image = clahe(croppedImage)

            #Thresholding
            result = five_note(clahe_image)

            #Temp file for ocr
            cv2.imwrite(temp_file, result)
            #Temp file for gui
            gui_size = image

            cv2.imwrite(temp_file_gui,gui_size)
        except:
            print("Error  with GUI, restarting. Maybe no image selected?")
            error_gui()

def crop_right_corner(result):
    try:
        H,W = result.shape[:2]
        half_x = int(W/2)
        half_y = int(H/3)
        crop_result = result[0:half_y,half_x:W]

        return(crop_result)
    except:
        print("Could not crop result, returning original image")
        return(result)

def main():
    #temp variables
    try:
        dbmod.database_conn()
        print("Database connected")
    except:
        print("Databse not connected")

    #Getting user input and saving an original copy of it
    image = guimod.start_gui()
    image = resize(image)


    guimod.popup()
    fromCenter = False
    r = cv2.selectROI(image, fromCenter)

    if r is not (0,0,0,0):
        imCrop = image[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
    else:
        imCrop=image

    cv2.destroyAllWindows()
    # Display cropped image

    imCrop = image


    image = imCrop
    original = image

    choice = guimod.multichoice_box()
    if(choice == "€5 - Back"):
        text_extract(image, "Banknotes/5_Back/")
        folder = "Banknotes/5_Back/"
        value = 5


    elif(choice =="€5 - Front"):
        text_extract(image, "Banknotes/5_Front/")
        folder = "Banknotes/5_Front/"
        value = 5


    elif(choice =="€10 - Back"):
        text_extract(image, "Banknotes/10_Back/")
        folder = "Banknotes/10_Back/"
        value = 10


    elif(choice =="€10 - Front"):
        text_extract(image, "Banknotes/10_Front/")
        folder = "Banknotes/10_Front/"
        value = 10


    elif(choice =="€20 - Back"):
        text_extract(image, "Banknotes/20_Back/")
        folder = "Banknotes/20_Back/"
        value = 20


    elif(choice =="€20 - Front"):
        text_extract(image, "Banknotes/20_Front/")
        folder = "Banknotes/20_Front/"
        value = 20


    elif(choice =="€50 - Back"):
        text_extract(image, "Banknotes/50_Back/")
        folder ="Banknotes/50_Back/"
        value = 50


    elif(choice =="€50 - Front"):
        text_extract(image, "Banknotes/50_Front/")
        folder ="Banknotes/50_Front/"
        value = 50


    elif(choice =="€100 - Back"):
        text_extract(image, "Banknotes/100_Back/")
        folder ="Banknotes/100_Back/"
        value = 100


    elif(choice =="€100 - Front"):
        text_extract(image, "Banknotes/100_Front/")
        value = 100
        folder ="Banknotes/100_Front/"


    # Include tesseract executable in your path
    pytesseract.pytesseract.tesseract_cmd = r"c:\Program Files\Tesseract-OCR\tesseract.exe"
    # Create an image object of PIL library
    image = Image.open(temp_file)

    try:
        serial_number = pytesseract.image_to_string(image, lang=None, config  = ' --dpi 300  --psm 3  --oem 3 -c  tessedit_char_whitelist=0123456789ABCDEFGHJKLMNPRTSUZYXWVRQP load_system_dawg=0 load_freq_dawg=0 ')
        print(serial_number)
        words = serial_number.split()

        serial_number = words[0]
    except:
        ("Error reading characters from banknote")

    try:
        banknote.validate(serial_number)
        real_note=True
    except:
        print("Invalid Serial Number")
        real_note=False

    if real_note is False:
        threshold=fem.feature_extract(original,folder)
    else:
        threshold="100"

    dt = None

    if len(serial_number)>=11:
        try:
            dt = dbmod.database_select(serial_number)
        except:
            print("Error selecting or no data found")

        if dt is None:
            dbmod.database_insert(serial_number, real_note, value)

    guimod.end_gui(temp_file_gui,serial_number,real_note,threshold,dt)

def five_note(original):

    img = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    img = cv2.normalize(img,None,0,255,cv2.NORM_MINMAX)

    blur = cv2.bilateralFilter(img,9,75,75)
    ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    return(th3)

def convert_gray(image):
    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    return(image)

def resize(image):
    resized=cv2.resize(image,(1600,900), interpolation = cv2.INTER_AREA )
    return(resized)

def clahe(image):
    try:
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        lab_planes = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(16,16))
        lab_planes[0] = clahe.apply(lab_planes[0])
        lab = cv2.merge(lab_planes)
        bgr = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        return(bgr)
    except:
        print("Error normalizing")
        return(image)


def error_gui():
     box_choices =["Restart","Exit Program"]
     user_choice =gui.buttonbox("There was an error with the program, please make sure you're inputting an image file",choices = box_choices)
     if user_choice == "Restart":
         try:
			 #Call open_image method which returns the image variables
             main()
         except:
             print("Error restarting, shutting down")
     elif user_choice=="Exit Program":
        raise SystemExit

if __name__ == '__main__':
    main()
