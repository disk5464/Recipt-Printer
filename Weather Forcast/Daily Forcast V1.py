#This script gets today's weather from NOWA then sends it to the receipt printer. The idea is to have it run automatically each morning.
#Created by: Disk5464
#Version 1.0: Inital Commit
#Version 1.1: Added the printer portion, Added comments, Changed the name of the printer
###############################################
#Import the libaries
import requests
from escpos.printer import Network
from PIL import Image, ImageDraw

###############################################
#Set up the headers and endpoint for the API
headers = {'User-Agent' : 'myapp'}
endpoint = 'https://api.weather.gov/gridpoints/LWX/39.7456,-97.0892/forecast'

#Send out the request and store the response as Json, then filter it into a smaller dict
response = requests.get(endpoint, headers = headers)
data = response.json()
todaysweather = data['properties']['periods'][0]

##############################################################################
#Define the printer IP and model. Also set the text alignment / font.
kitchenPrinter = Network("192.168.50.102", profile="TM-T88V")
kitchenPrinter.set(align="left", bold=False, double_width=False)

#Send the weather info we want to print to the printer
kitchenPrinter.text(f"{todaysweather['shortForecast']}\n")
kitchenPrinter.text(f"Temperature: {todaysweather['temperature']} F\n")
kitchenPrinter.text(f"Chance of Rain: {todaysweather['probabilityOfPrecipitation']['value']}%\n")
kitchenPrinter.text(f"Wind: {todaysweather['windSpeed']}\n")
#kitchenPrinter.text(f"Detailed Forecast: {todaysweather['detailedForecast']}\n")

###############################################################################
#Cut the paper
kitchenPrinter.cut()