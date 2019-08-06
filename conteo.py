from PIL import Image, ImageDraw, ImageOps,ImageFilter
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.color import label2rgb
from numpy import array
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def mask(low, high):
	return [255 if low <= x <= high else 0 for x in range(0, 256)]

UMBRAL = [(0,30), (0,30), (0,30)]
class Semillero(object):
	def __init__(self, archivo):
		self.archivo = archivo
		self.img = Image.open(archivo)
		size = self.img.size
		# print(self.img.size)
		tam = 1600
		self.img = self.img.resize((tam, int(size[1] * tam / size[0]))) if size[0] > size[1] else  self.img.resize((int(size[0] * tam / size[1]),tam))
		# self.img = self.img.filter(ImageFilter.UnsharpMask(6,80))
		# self.img = self.img.filter(ImageFilter.GaussianBlur())
		# self.img = self.img.filter(ImageFilter.UnsharpMask(4))
		tamfilter = 3
		self.img = self.img.filter(ImageFilter.RankFilter(tamfilter, int(tamfilter*tamfilter/2)))
		# self.img = ImageOps.equalize(self.img)
		# self.img = ImageOps.autocontrast(self.img)
		# print(self.img.size)
		self.regiones = []
	def BuscarRegiones(self):
		mask_R = mask(UMBRAL[0][0], UMBRAL[0][1])
		mask_G = mask(UMBRAL[1][0], UMBRAL[1][1])
		mask_B = mask(UMBRAL[2][0], UMBRAL[2][1])
		self.img_binary = self.img.point(mask_R+mask_G+mask_B).convert('L').point([0]*255+[255])
		self.img_binary.save("binario.jpg")
		self.img_binary = self.img_binary.filter(ImageFilter.MaxFilter(5))
		self.img_binary = self.img_binary.filter(ImageFilter.MinFilter(5))
		self.img_binary.save("binario2.jpg")
		arr_binary = array(self.img_binary)
		arr_closed = closing(arr_binary)
		arr_labeled = label(arr_closed)
		self.regiones = regionprops(arr_labeled)
	def PromedioArea(self):
		# print("Calculando")
		self.prom = -1
		self.std = -1
		valores = []
		while self.std > self.prom * .5 or self.std == -1:
			valores = []
			for region in self.regiones:
				if (region.area > self.prom + self.std or region.area < self.prom - self.std) and self.prom != -1 and self.std != -1:
					continue
				valores.append(region.area)
			self.prom = np.mean(valores)
			self.std = np.std(valores)
		self.minimo = min(valores)
			# print("Promedio", self.prom,"std",self.std, valores)
	def Validas(self):
		return [ region for region in self.regiones if region.area < self.prom + self.std and region.area > self.prom - self.std ]
	def Procesar(self):
		# print("Procesando")
		self.BuscarRegiones()
		self.PromedioArea()
		validas = self.Validas()
		print("Cantidad validas", len(validas))
		fig, ax = plt.subplots()
		for p in [
		    [patches.Rectangle(
		        (r.bbox[1], r.bbox[0]),
		        r.bbox[3] - r.bbox[1],
		        r.bbox[2] - r.bbox[0],
		        fill=False,
		        edgecolor='blue',
		        alpha=.4
		    ), r.centroid] for r in validas]: 
		    ax.add_patch(p[0])
		    # plt.plot(p[1][1], p[1][0], 'bo')
		resto = [region for region in self.regiones if region not in validas and region.area > self.minimo - self.std]
		print("restos posibles", len(resto))
		for p in [
			[patches.Rectangle(
		        (r.bbox[1], r.bbox[0]),
		        r.bbox[3] - r.bbox[1],
		        r.bbox[2] - r.bbox[0],
		        fill=False,
		        edgecolor='red',
		        alpha=.4
		    ), r.centroid, r.image] for r in resto]:
		    ax.add_patch(p[0])
		    # plt.plot(p[1][1], p[1][0], 'ro')	
		plt.imshow(self.img)
		plt.show()
Semillero("imagen/IMG_20180118_090124.jpg").Procesar()
# Semillero("imagen/50.jpg").Procesar()
