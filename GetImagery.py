import requests
from pyproj import Proj, transform
import matplotlib.pyplot as plt
from scipy import ndimage
from io import BytesIO
from skimage import io


def GetMyCoords():
	# Get your coordinates according to your IP address
	coords = requests.get('https://freegeoip.net/csv/').text
	lat, lon = coords.split(',')[-3:-1]          
	lat, lon = float(lat), float(lon)
	return lat, lon

def ReprojectPoint(x, y, projIn, ProjOut):
	# Reproject to epsg:3035
	inProj = Proj(init=projIn)
	outProj = Proj(init=ProjOut)
	x, y = transform(inProj,outProj, x, y)
	return x, y

def GetSatImgry(x,y):
	# Create the bounding box
	diff = x * 0.0004
	x1,y1,x2,y2 = x - diff, y - diff, x + diff, y + diff
	bbox = "bbox={0},{1},{2},{3}".format(x1,y1,x2,y2)
	# Get satellite imagery from Copernicus and write to file-like object
	url = 'http://copernicus.discomap.eea.europa.eu/arcgis/rest/services/GioLand/VeryHighResolution2012/MapServer/export?dpi=96&transparent=true&format=png8&{0}&bboxSR=3035&imageSR=3035&size=3816%2C3816&f=image'.format(bbox)
	img = BytesIO()
	r = requests.get(url, stream=True)
	for chunk in r.iter_content(1024):
		img.write(chunk)
		
	imgArray = ndimage.imread(img, mode='RGB')
	
	return img, imgArray

def PlotImage(img):
	imgry = io.imread(img)
	plt.imshow(imgry)
	plt.axis("off")
	plt.show()
	return
	
def analyzeImgArray(imgArray):
	print(type(imgArray))
	
	
	
	return imgArray
	
def main():
	lat,lon = GetMyCoords()
	x,y = ReprojectPoint(lon, lat, "epsg:4326", "epsg:3035")
	img, imgArray = GetSatImgry(x,y)
	PlotImage(img)
	analyzeImgArray(imgArray)
	
	return

if __name__ == '__main__':
	main()