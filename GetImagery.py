import requests
from pyproj import Proj, transform
import matplotlib.pyplot as plt
from scipy import ndimage, signal
from io import BytesIO
from skimage import io
import numpy as np


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
		
	# imgArray = ndimage.imread(img, mode='RGB')
	imgArray = ndimage.imread(img, mode='RGB')
	
	
	return img, imgArray

def PlotImage(img):
	imgry = io.imread(img)
	plt.imshow(imgry)
	plt.axis("off")
	plt.show()
	return
	
def analyzeImgArray(imgArray):
	# print(type(imgArray))
	# imgArray_gray = np.dot(imgArray[...,:3], [0.299, 0.587, 0.114])
	# plt.imshow(imgArray_gray, cmap=plt.cm.gray, vmin=30, vmax=200)
	# plt.contour(imgArray_gray, [50, 150])
	plt.imshow(imgArray)
	n=100
	sobel_x = np.c_[
		[-1,0,1],
		[-2,0,2],
		[-1,0,1]
	]

	sobel_y = np.c_[
		[1,2,1],
		[0,0,0],
		[-1,-2,-1]
	]

	ims = []
	for d in range(3):
		sx = signal.convolve2d(imgArray[:,:,d], sobel_x, mode="same", boundary="symm")
		sy = signal.convolve2d(imgArray[:,:,d], sobel_y, mode="same", boundary="symm")
		ims.append(np.sqrt(sx*sx + sy*sy))

	im_conv = np.stack(ims, axis=2).astype("uint8")

	plti(im_conv)
	plt.axis("off")
	plt.show()
	
	return imgArray
	
def plti(im, h=8, **kwargs):
    """
    Helper function to plot an image. By: http://www.degeneratestate.org/posts/2016/Oct/23/image-processing-with-numpy/
    """
    y = im.shape[0]
    x = im.shape[1]
    w = (y/x) * h
    plt.figure(figsize=(w,h))
    plt.imshow(im, interpolation="none", **kwargs)
    plt.axis('off')
	
def main():
	lat,lon = GetMyCoords()
	x,y = ReprojectPoint(lon, lat, "epsg:4326", "epsg:3035")
	img, imgArray = GetSatImgry(x,y)
	# PlotImage(img)
	analyzeImgArray(imgArray)
	
	return

if __name__ == '__main__':
	main()