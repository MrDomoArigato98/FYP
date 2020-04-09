# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 14:39:38 2020

@author: Dominik
"""
import easygui as gui
import sys
import cv2
import string
import re
import os
import main as cvmod
from datetime import datetime

#open the image through user choice
def open_image():
    f = gui.fileopenbox()
    image = cv2.imread(f)
    return(image)

def start_gui():
    #Choices for the GUI buttons,requires an array
    box_choices =["Choose image","Exit Program"]
    title = "Authenti-Note"
    user_choice =gui.buttonbox("Welcome to Authenti-note. \nPlease insert you banknote image",title,choices = box_choices)
    if user_choice == "Choose image":
        try:
			#Call open_image method which returns the image variables
            image  = open_image()
            return(image)
        except:
            cvmod.error_gui()
            sys.exit("Error opening image")
    elif user_choice=="Exit Program":
        sys.exit("User choice to exit, closing")

def multichoice_box():
    msg = "What denomination & Side is the banknote?"
    title = "User Options"
    choices = ["€5 - Back","€5 - Front",
    "€10 - Back", "€10 - Front",
    "€20 - Back","€20 - Front",
    "€50 - Back","€50 - Front",
    "€100 - Back","€100 - Front"]
    choice = gui.choicebox(msg, title, choices)

    msg = ("Your choice is: " + str(choice))
    title = "Please confirm your choice"


    if(choice is None):
        sys.exit("No user choice, closing")

    if gui.ccbox(msg, title):     # show a Continue/Cancel dialog
        return(choice)  # user chose Continue
    else:
        sys.exit("User choice to exit, closing") # user chose Cancel

def end_gui(temp_file_gui,serial_number,real_note,threshold,dt):
	#Concatenate the strings together for the result

    if real_note is True:
        checksum="Valid serial number"
    else:
        checksum="None found"

    if (len(serial_number)>13 or serial_number is None):
        serial_number="None found"
    if dt is None:
        dt = datetime.now()
    x = re.findall("[0123456789ABCDEFGHJKLMNPRTSUZYXWVRQP]", serial_number)
    if(x):

        program_reply=("The Serial Number is: "+ serial_number + "\nThis banknote is: "+threshold+"% Authentic \nChecksum on serial number: "+checksum+"\nThis note was tested on: "+dt.strftime("%d-%m-%Y %H:%M"))
    	#Box choices in GUI, requires an array
        box_choices =["Main Menu","Exit Program"]
    	#Display buttonbox, with image,and choices
        user_choice = gui.buttonbox(program_reply,image = temp_file_gui,choices = box_choices)
    	#Remove the image that was written for displaying circles
        os.remove(temp_file_gui)
    else:
        program_reply=("Could not read the serial number \nThis banknote is: "+threshold+"% Authentic \nChecksum on serial number: "+checksum)
    	#Box choices in GUI, requires an array
        box_choices =["Main Menu","Exit Program"]
    	#Display buttonbox, with image,and choices
        user_choice =gui.buttonbox(program_reply,image = temp_file_gui,choices = box_choices)
    	#Remove the image that was written for displaying circles
        os.remove(temp_file_gui)
	#Checks which buttons were pressed
    if user_choice =="Main Menu":
        cvmod.main()
    else:
        sys.exit("Exiting by user choice, closing program")

def popup():
     msg = "In the next menu, please crop your banknote by clicking and dragging to crop the banknote.\n \nOnce you are done, please press ENTER"
     title = "Instructions"
     if gui.ccbox(msg, title):     # show a Continue/Cancel dialog
         print("Continuing...")
     else:
        sys.exit("User choice to exit, closing") # user chose Cancel
