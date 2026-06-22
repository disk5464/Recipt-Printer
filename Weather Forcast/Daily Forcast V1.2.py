#This script gets today's weather from NOWA then sends it to the receipt printer. The idea is to have it run automatically each morning.
#Created by: Disk5464
#Version 1.0: Inital Commit
#Version 1.1: Added the printer portion, Added comments, Changed the name of the printer
#Version 1.2: Added in emoticon support via  
###############################################################################
#Import the libaries
import requests
from escpos.printer import Network
from PIL import Image, ImageDraw

###############################################################################
#Define a function to generate the icon for today's weather.
def make_icon(kind, size=100):
    
    # 1-bit image, white background
    img = Image.new("1", (size, size), 1)  
    d = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2

    #Create a basic black circle with straight lines arround it for the rays
    if kind == "sunny":
        r = size // 5
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=0)
        for angle in range(0, 360, 45):
            import math
            x1 = cx + (r + 4) * math.cos(math.radians(angle))
            y1 = cy + (r + 4) * math.sin(math.radians(angle))
            x2 = cx + (r + 14) * math.cos(math.radians(angle))
            y2 = cy + (r + 14) * math.sin(math.radians(angle))
            d.line([x1, y1, x2, y2], fill=0, width=3)
    #Create 3 black circles for the clouds
    elif kind == "cloudy":
        d.ellipse([cx - 22, cy - 5, cx + 2, cy + 15], fill=0)
        d.ellipse([cx - 5, cy - 15, cx + 20, cy + 12], fill=0)
        d.ellipse([cx + 5, cy - 2, cx + 25, cy + 16], fill=0)
    
    #Same thing as above but add in 3 long lines for rain drops.
    elif kind == "rain" or kind == "showers":
        d.ellipse([cx - 22, cy - 18, cx + 2, cy + 2], fill=0)
        d.ellipse([cx - 5, cy - 28, cx + 20, cy - 1], fill=0)
        d.ellipse([cx + 5, cy - 15, cx + 25, cy + 3], fill=0)
        for dx in (-15, 0, 15):
            d.line([cx + dx, cy + 10, cx + dx - 5, cy + 25], fill=0, width=3)
    
    #Same thing as above but add in 3 short lines for snow.
    elif kind == "snow":
        d.ellipse([cx - 22, cy - 18, cx + 2, cy + 2], fill=0)
        d.ellipse([cx - 5, cy - 28, cx + 20, cy - 1], fill=0)
        d.ellipse([cx + 5, cy - 15, cx + 25, cy + 3], fill=0)
        for dx in (-15, 0, 15):
            d.ellipse([cx + dx - 2, cy + 18, cx + dx + 2, cy + 22], fill=0)
    
    #Same thing as for cloudy but add in a lightning bolt.
    elif kind == "thunderstorms":
        d.ellipse([cx - 22, cy - 22, cx + 2, cy - 2], fill=0)
        d.ellipse([cx - 5, cy - 32, cx + 20, cy - 5], fill=0)
        d.ellipse([cx + 5, cy - 19, cx + 25, cy - 1], fill=0)
        d.polygon([(cx, cy), (cx - 8, cy + 15), (cx + 2, cy + 15), (cx - 6, cy + 30)], fill=0)

    #Send back the icon to where it was called from.
    return img

##############################################################################
#Define the printer IP and model. Also set the text alignment / font.
kitchenPrinter = Network("192.168.50.102", profile="TM-T88V")
kitchenPrinter.set(align="left", bold=False, double_width=False)

###############################################
#Set up the headers and endpoint for the API
headers = {'User-Agent' : 'myapp'}
endpoint = 'https://api.weather.gov/gridpoints/LWX/116,84/forecast'

#Send out the request and store the response as Json, then filter it into a smaller dict
response = requests.get(endpoint, headers = headers)
data = response.json()
todaysweather = data['properties']['periods'][0]

#Read the weather report and create an icon bassed on the weather
if "cloudy" in todaysweather['shortForecast'].lower():
    icon = make_icon("cloudy")
elif "sunny" in todaysweather['shortForecast'].lower():
    icon = make_icon("sunny")
elif "thunderstorm" in todaysweather['shortForecast'].lower():
    icon = make_icon("thunderstorms")
elif "showers" in todaysweather['shortForecast'].lower() or "rain" in todaysweather['shortForecast'].lower():
    icon = make_icon("rain")
elif "snow" in todaysweather['shortForecast'].lower():
    icon = make_icon("snow")

#Send the weather info we want to print to the printer
kitchenPrinter.image(icon, center=True)
kitchenPrinter.text(f"{todaysweather['shortForecast']}\n")
kitchenPrinter.text(f"Temperature: {todaysweather['temperature']} F\n")
kitchenPrinter.text(f"Chance of Rain: {todaysweather['probabilityOfPrecipitation']['value']}%\n")
kitchenPrinter.text(f"Wind: {todaysweather['windSpeed']}\n")
#kitchenPrinter.text(f"Detailed Forecast: {todaysweather['detailedForecast']}\n")

###############################################################################
#Cut the paper
kitchenPrinter.cut()