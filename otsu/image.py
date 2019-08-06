from skimage import filters, io, exposure
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
import numpy as np
from matplotlib.path import Path
import PIL

def get_imagen_pil(ruta):
	return PIL.Image.open(ruta)

def get_imagen_ski(ruta, modo='L'):
	return io.imread(ruta, modo)

def umbral_otsu(img_ski):
	return filters.threshold_otsu(img_ski)

def otsu(img_ski, valor = None, q=None):
	if(valor == None):
		valor = filters.threshold_otsu(img_ski)
	else:
		valor = valor / 255
	img_binary = img_ski < valor
	if(q!=None):
		q.put("Agrupando")
	img_closed = closing(img_binary, square(3))
	if(q!=None):
		q.put("Etiquetando")
	img_labeled = label(img_closed)
	if(q!=None):
		q.put("Reconociendo semillas")
	return regionprops(img_labeled)

def isodata(img_ski):
	valor = filters.threshold_isodata(img_ski)
	img_binary = img_ski < valor
	img_closed = closing(img_binary, square(3))
	img_labeled = label(img_closed)
	return regionprops(img_labeled)

def regiones_con_umbral(img_ski, umbral):
	img_binary = img_ski < umbral
	img_closed = closing(img_binary, square(3))
	img_labeled = label(img_closed)
	return regionprops(img_labeled)

def cortar(img , puntos):

	nr, nc = img.shape
	ygrid, xgrid = np.mgrid[:nr, :nc]
	xypix = np.vstack((xgrid.ravel(), ygrid.ravel()))
	pth = Path(puntos, closed=False)

	mask = pth.contains_points(xypix)

	mask = mask.reshape(img.shape)

	masked = np.ma.masked_array(img, ~mask)

	xmin, xmax = int(xc.min()), int(np.ceil(xc.max()))
	ymin, ymax = int(yc.min()), int(np.ceil(yc.max()))
	trimmed = masked[ymin:ymax, xmin:xmax]
	return trimmed