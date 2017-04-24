import requests
from pyproj import Proj, transform
import matplotlib.pyplot as plt
from skimage import io
import georasters as gr
import pandas as pd


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

def GetMySatImgryURL(x,y):
	# Create the bounding box
	diffx = x * 0.0004
	diffy = y * 0.0004
	x1,y1,x2,y2 = x - diffx, y - diffy, x + diffx, y + diffy
	bbox = "bbox={0},{1},{2},{3}".format(x1,y1,x2,y2)
	# Get satellite imagery from Copernicus
	url = 'http://copernicus.discomap.eea.europa.eu/arcgis/rest/services/GioLand/VeryHighResolution2012/MapServer/export?dpi=96&transparent=true&format=png8&{0}&bboxSR=3035&imageSR=3035&size=3816%2C3816&f=image'.format(bbox)
	return url

def PlotImageFromURL(url):
	# Load image from url
	imgry = io.imread(url)
	plt.imshow(imgry)
	plt.show()
	return

def img2df(url):
	# raster = io.imread(url)
	data = gr.from_file(url)
	df = data.to_pandas()
	return df

def dfKernel(df, size, function):
	if size % 2 == 0:
		print("Only uneven kernel size is allowed")
		return 

	Xmax = int(max(df['x'])) - (size-1)//2
	Ymax = int(max(df['y'])) - (size-1)//2
	df.set_index('y')
	output = pd.DataFrame(columns=['x','y','value'])
	for y in range(Ymax):
		rows = df.loc[df['y'].isin(range(y, y+size))]
		for x in range(Xmax):
			kernel = rows.loc[df['x'].isin(range(x, x+size))]
			print(kernel)
			output['x'] = x
			output['y'] = y 
			output['value'] = function(kernel)
	return

def avg(lst):
	pass
	return 

def main():
	lat,lon = GetMyCoords()
	x,y = ReprojectPoint(lon, lat, "epsg:4326", "epsg:3035")
	url = GetMySatImgryURL(x,y)
	df = img2df(url)
	# print(df.head)
	# PlotImageFromURL(url)
	dfKernel(df,3,avg)
	return

if __name__ == '__main__':
	main()