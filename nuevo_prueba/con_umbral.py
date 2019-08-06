from PIL import Image, ImageDraw, ImageOps,ImageFilter
from funciones import Regiones, Mediciones, CheckRestos2
from muestra import Muestra
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
# IMG_20180118_084215 ~ 730 semillas
ruta = "../imagen/IMG_20180118_084208.jpg"

def mask(low, high):
	return [255 if low <= x <= high else 0 for x in range(0, 256)]
img = Image.open(ruta)
# tamfilter = 5
# img = img.filter(ImageFilter.RankFilter(tamfilter, int(tamfilter*tamfilter/2)))
# Escalar
size = img.size
tam = 4000
img = img.resize((tam, int(size[1] * tam / size[0]))) if size[0] > size[1] else  img.resize((int(size[0] * tam / size[1]),tam))

muestras = Muestra(img)
areas = [r[1] for r in muestras]
colores = [r[0] for r in muestras]
UMBRAL = (np.mean([c[0] for c in colores]),np.mean([c[1] for c in colores]),np.mean([c[2] for c in colores]))
area_min = np.mean(areas)

print(UMBRAL, area_min, areas)

# area_min = 16
# UMBRAL = (75,75,75)

mask_R = mask(0, UMBRAL[0])
mask_G = mask(0, UMBRAL[1])
mask_B = mask(0, UMBRAL[2])

img_binary = img.point(mask_R+mask_G+mask_B).convert('L').point([0]*255+[255])

regiones = Regiones(img_binary, area_min)
media, std, validos = Mediciones(regiones,area_min)

print("contadas", len(validos))
print("calculando restos")
# restos = [region.label for region in regiones if region.label not in validos and region.area > media - std * 3] #and region.area > area_min]
restos = [region for region in regiones if region.label not in validos and region.area > media - std * 3 and region.area > area_min - std/3]
print("restos", len(restos))
# total = len(validos) + CheckRestos(img,restos,media,std)
# print("total",total)
corregidas = CheckRestos2(img,restos,media,std)
print(len(validos) + sum([x[1] for x in corregidas]))
fig, ax = plt.subplots()
plt.imshow(img)

paraimprimir = {r.label:[r.bbox,r.centroid] for r in restos}

for p in [
		[patches.Rectangle(
		    (r.bbox[1], r.bbox[0]),
		    r.bbox[3] - r.bbox[1],
		    r.bbox[2] - r.bbox[0],
		    fill=False,
		    edgecolor='blue',
		    alpha=.4
		),r.centroid] for r in regiones if r.label in validos]: 
		ax.add_patch(p[0])
		# plt.text(p[1][1], p[1][0], 1, ha="center", size=10, color="red")
for r in corregidas:
	ax.add_patch(patches.Rectangle(
		(paraimprimir[r[0]][0][1], paraimprimir[r[0]][0][0]),
	    paraimprimir[r[0]][0][3] - paraimprimir[r[0]][0][1],
	    paraimprimir[r[0]][0][2] - paraimprimir[r[0]][0][0],
	    fill=False,
	    edgecolor='red',
	    alpha=.4))
	plt.text(
		paraimprimir[r[0]][1][1], 
		paraimprimir[r[0]][1][0],
		r[1], ha="center", size=10, color="red")		
plt.show()