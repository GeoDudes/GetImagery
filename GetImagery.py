import requests
from pyproj import Proj, transform
import matplotlib.pyplot as plt
from skimage import io

GetMyCoords():
	# Get your coordinates according to your IP address
	coords = requests.get('https://freegeoip.net/csv/').text
	lat, lon = coords.split(',')[-3:-1]          
	lat, lon = float(lat), float(lon)
	return lat, lon

ReprojectPoint(x, y, projIn, ProjOut):
	# Reproject to epsg:3035
	inProj = Proj(init=projIn)
	outProj = Proj(init=ProjOut)
	x, y = transform(inProj,outProj, x, y)
	return x, y

GetMySatImgryURL(x,y):
	# Create the bounding box
	diffx = x * 0.0011318633808645777
	diffy = y * 0.0003964062069618698
	x1,y1,x2,y2 = x - diffx, y - diffy, x + diffx, y + diffy
	bbox = "bbox={0},{1},{2},{3}".format(x1,y1,x2,y2)
	url = 'http://copernicus.discomap.eea.europa.eu/arcgis/rest/services/GioLand/VeryHighResolution2012/MapServer/export?dpi=96&transparent=true&format=png8&{0}&bboxSR=3035&imageSR=3035&size=1908%2C544&f=image'.format(bbox)
	return url

PlotImageFromURL(url):
	# Get satellite imagery from Copernicus
	imgry = io.imread(url)
	plt.imshow(imgry)
	plt.show()
	return

main():
	lat,lon = GetMyCoords()
	x,y = ReprojectPoint(lon, lat, "epsg:4326", "epsg:3035")
	url = GetMySatImgrURL(x,y)
	PlotImageFromURL(url)


if __name__ == '__main__':
	main()