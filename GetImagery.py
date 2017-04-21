import pandas as pd
import json
import requests
from pyproj import Proj, transform

# Get your IP address according to the IP 
coords = requests.get('https://freegeoip.net/csv/').text
place = coords.split(',')[-4]
lat, lon = coords.split(',')[-3:-1]          
lat, lon = float(lat), float(lon)

# Reproject to epsg:3035
inProj = Proj(init='epsg:4326')
outProj = Proj(init='epsg:3035')
x, y = transform(inProj,outProj,lon, lat)

# Create the bounding box
diffx = x * 0.0011318633808645777
diffy = y * 0.0003964062069618698
x1,y1,x2,y2 = x - diffx, y - diffy, x + diffx, y + diffy
bbox = "bbox={0},{1},{2},{3}".format(x1,y1,x2,y2)

# Get satellite imagery from Copernicus
imgry = io.imread('http://copernicus.discomap.eea.europa.eu/arcgis/rest/services/GioLand/VeryHighResolution2012/MapServer/export?dpi=96&transparent=true&format=png8&bbox={0}%2C{1}%2C{2}%2C{3}&bboxSR=3035&imageSR=3035&size=1908%2C544&f=image'.format(x-1000,y-1000,x+400,y+400))
plt.imshow(imgry)
plt.show()