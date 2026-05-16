#This script will take an input and send it to the Epson recipt printer
#Libary Documentation: https://python-escpos.readthedocs.io/en/latest/user/methods.html
#                      https://winslowjosiah.com/blog/2024/08/27/i-got-a-receipt-printer/
#                      https://www.youtube.com/watch?v=7KtyekivpRM
###############################################################################
#Import the library
from escpos.printer import Network
###############################################################################
#Define the printer's IP and the profile which is just the model number
kitchen = Network("192.168.1.176", profile="TM-T88V") 

#Set the alignment, just incase it was set to something else on the last run
kitchen.set(align="left")

#Define what you want to print \n adds a new line at the end
kitchen.text("Hello World\n")

#If you want to do an image this is how you do it. The high density settings will try and print the image in full size. If its too big it just stretches the image
#kitchen.image("C:\\temp\\Jaz.jpg", high_density_vertical=False, high_density_horizontal=False)
#kitchen.image("C:\\temp\\Jaz.jpg")

#This tells the printer to print and then cut the reciept.
kitchen.cut()