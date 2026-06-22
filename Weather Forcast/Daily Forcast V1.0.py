#This script gets today's weather from NOWA then sends it to the receipt printer. The idea is to have it run automatically each morning.
#Created by: Disk5464
#Version 1.0: Inital Commit
###############################################
from escpos.printer import Network
from PIL import Image, ImageDraw

###############################################################################
kitchen = Network("192.168.50.102", profile="TM-T88V")
kitchen.set(align="center")

###############################################################################
# Weather icon generator - draws simple monochrome icons, no fonts needed
###############################################################################
def make_icon(kind, size=100):
    img = Image.new("1", (size, size), 1)  # 1-bit image, white background
    d = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2

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

    elif kind == "cloudy":
        d.ellipse([cx - 22, cy - 5, cx + 2, cy + 15], fill=0)
        d.ellipse([cx - 5, cy - 15, cx + 20, cy + 12], fill=0)
        d.ellipse([cx + 5, cy - 2, cx + 25, cy + 16], fill=0)

    elif kind == "rain":
        d.ellipse([cx - 22, cy - 18, cx + 2, cy + 2], fill=0)
        d.ellipse([cx - 5, cy - 28, cx + 20, cy - 1], fill=0)
        d.ellipse([cx + 5, cy - 15, cx + 25, cy + 3], fill=0)
        for dx in (-15, 0, 15):
            d.line([cx + dx, cy + 10, cx + dx - 5, cy + 25], fill=0, width=3)

    elif kind == "snow":
        d.ellipse([cx - 22, cy - 18, cx + 2, cy + 2], fill=0)
        d.ellipse([cx - 5, cy - 28, cx + 20, cy - 1], fill=0)
        d.ellipse([cx + 5, cy - 15, cx + 25, cy + 3], fill=0)
        for dx in (-15, 0, 15):
            d.ellipse([cx + dx - 2, cy + 18, cx + dx + 2, cy + 22], fill=0)

    elif kind == "storm":
        d.ellipse([cx - 22, cy - 22, cx + 2, cy - 2], fill=0)
        d.ellipse([cx - 5, cy - 32, cx + 20, cy - 5], fill=0)
        d.ellipse([cx + 5, cy - 19, cx + 25, cy - 1], fill=0)
        d.polygon([(cx, cy), (cx - 8, cy + 15), (cx + 2, cy + 15), (cx - 6, cy + 30)], fill=0)

    return img

###############################################################################
# Print a weather line: icon + label
###############################################################################
def print_weather(kind, label):
    icon = make_icon(kind)
    kitchen.image(icon)
    kitchen.text(f"{label}\n")

print_weather("sunny", "Sunny - 78F")
print_weather("cloudy", "Cloudy - 65F")
print_weather("rain", "Rain - 58F")
print_weather("snow", "Snow - 32F")
print_weather("storm", "Storm - 45F")





kitchen.cut()