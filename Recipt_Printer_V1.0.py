#This script will take an input from a streamlit website and send it to a Epson recipt printer to be printed
#Libary Documentation: https://python-escpos.readthedocs.io/en/latest/user/methods.html
#                      https://winslowjosiah.com/blog/2024/08/27/i-got-a-receipt-printer/
#                      https://www.youtube.com/watch?v=7KtyekivpRM
#                      https://en.wikipedia.org/wiki/Block_Elements
#                      https://medium.com/@dongaresuyash/dockerizing-your-streamlit-app-a-beginner-friendly-guide-b63d1214d0ad
###############################################################################
#Import the libaries
import streamlit as st
from escpos.printer import Network

###############################################################################
#Define the streamlit header and set up the text input box
st.header("What do you want to be reminded of?", divider="blue", width ="content")
text_input = st.text_input("    ")

###############################################################################
#When the user clicks presses enter on the keyboard the input is translated into a print command
if text_input:
    #Write to the website what was sent to the printer
    st.write("Info sent to printer: ", text_input)
    
    #Set the defaults for the printer. This is so that the printer is reset back to a known baseline
    #kitchen = Network("192.168.1.176", profile="TM-T88V") 
    kitchen = Network("10.0.0.67", profile="TM-T88V") 
    kitchen.set(align="left", bold=False, double_width=False)
    
    #Set the setting for the header, then print it
    kitchen.set(align="left", bold=True, double_width=True)
    kitchen.text("█████████████████████\n")
    
    #Set the settings for the body, then print it
    kitchen.set(align="center", bold=False, double_width=False)
    kitchen.text(text_input + "\n")
    
    #Set the settings for the footer, then print it
    kitchen.set(align="left", bold=True, double_width=True)
    kitchen.text("█████████████████████\n")
    
    #Send the print command and cut the paper
    kitchen.cut()