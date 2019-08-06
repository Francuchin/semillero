from PIL import Image, ImageDraw, ImageOps
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
def distancia(x, y): 
	return sqrt( sum( [ (xi - yi)**2 for xi, yi in zip(x, y) ] ) ) 

UMBRAL = [(0,80), (0,80), (0,80)]

IMAGENES = [
'IMG_20180118_084215',
'IMG_20180118_084153',
'IMG_20180118_084208',
'IMG_20180118_084236',
'IMG_20180118_084238',
'IMG_20180118_084317',
'IMG_20180118_084324',
'IMG_20180118_084342',
'IMG_20180118_084416',
'IMG_20180118_085605',
'IMG_20180118_090124',
'IMG_20180118_090127',
]
maxDist = -1

class Semillero(object):
	def __init__(self, archivo , cosopinba):
		self.cosopinba = cosopinba
		self.archivo = archivo
		if isinstance(archivo, str):
			self.img = ImageOps.autocontrast(Image.open(archivo))
		else:
			self.img = archivo
		mask_R = mask(UMBRAL[0][0], UMBRAL[0][1])
		mask_G = mask(UMBRAL[1][0], UMBRAL[1][1])
		mask_B = mask(UMBRAL[2][0], UMBRAL[2][1])
		self.img_binary = self.img.point(mask_R+mask_G+mask_B).convert('L').point([0]*255+[255])

	def contenedor(self):
		area_min_contenedor = int(max(self.img.size) / 22)
		arr_binary = array(self.img_binary)
		arr_closed = closing(arr_binary, square(area_min_contenedor))
		arr_labeled = label(arr_closed)
		regiones = regionprops(arr_labeled)
		_contenedor = None
		for region in regiones:
			if region.area < area_min_contenedor: continue
			_contenedor = region if _contenedor==None or _contenedor.area < region.area else _contenedor
		b = _contenedor.bbox if _contenedor != None else None
		if b != None :
			xa = b[1] - 2 if b[1] - 2 >= 0 else 0
			ya = b[0] - 2 if b[0] - 2 >= 0 else 0
			xb = b[3] + 2 if b[3] + 2 <= self.img.size[0] else self.img.size[0]
			yb = b[2] + 2 if b[2] + 2 <= self.img.size[1] else self.img.size[1]
		return  [xa,ya,xb,yb] if _contenedor != None else [0,0,self.img.size[1],self.img.size[0]]

	def procesar(self):		
		fig, ax = plt.subplots()
		arr_binary = array(self.img_binary)
		arr_closed = closing(arr_binary, square(3))
		arr_labeled = label(arr_closed)
		regiones = regionprops(arr_labeled)
		prom = -1
		std = -1
		valores = []
		while std > 15 or std == -1:
			valores = []
			for region in regiones:
				if (region.area > prom + std or region.area < prom - std) and prom != -1 and std != -1:
					continue
				valores.append(region.area)
			prom = np.mean(valores)
			std = np.std(valores)

		draw = ImageDraw.Draw(self.img)
		semillas = 0
		for region in regiones:
			if region.area > prom + std * 1.5 or region.area < prom - std * 1.5:
				continue
			semillas+=1
			centro=region.centroid[::-1]
			bbox=region.bbox
			xa = bbox[1] - 1 if bbox[1] - 1 >= 0 else 0
			ya = bbox[0] - 1 if bbox[0] - 1 >= 0 else 0
			xb = bbox[3] + 1 if bbox[3] + 1 < self.img.size[0] else self.img.size[0] - 1
			yb = bbox[2] + 1 if bbox[2] + 1 < self.img.size[1] else self.img.size[1] - 1
			color = [int((w + x + y + z)/4) for w, x, y, z in zip(
				self.img.getpixel((xa,ya)), 
				self.img.getpixel((xa,yb)), 
				self.img.getpixel((xb,ya)), 
				self.img.getpixel((xb,yb))
				)]
			draw.rectangle([xa,ya,xb,yb], outline=None, fill=(color[0],color[1],color[2]))
		del draw
		plt.imshow(self.img)#.crop(self.contenedor()))
		# plt.show()
		plt.savefig("cosopinba\\"+str(self.cosopinba)+".jpg",dpi=640)
		return [semillas, len(regiones) - semillas ,self.img]#.crop(self.contenedor())]

img = Semillero("imagen/"+IMAGENES[2]+".jpg",0)
resultados = img.procesar()

semillas = resultados[0]
while(resultados[1]>20):
	print("subres:",resultados[0],resultados[1])
	img = Semillero(resultados[2],img.cosopinba+1)
	resultados = img.procesar()
	semillas += resultados[0]
print("Semillas contadas", semillas)
# plt.imshow(resultados[2])
# plt.show()