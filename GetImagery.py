import requests
from pyproj import Proj, transform
import matplotlib.pyplot as plt
from skimage import io

# Get your IP address according to the IP 
coords = requests.get('https://freegeoip.net/csv/').text
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
imgry = io.imread('http://copernicus.discomap.eea.europa.eu/arcgis/rest/services/GioLand/VeryHighResolution2012/MapServer/export?dpi=96&transparent=true&format=png8&{0}&bboxSR=3035&imageSR=3035&size=1908%2C544&f=image'.format(bbox))
plt.imshow(imgry)
plt.show()