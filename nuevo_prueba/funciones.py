from PIL import Image, ImageDraw, ImageOps,ImageFilter, ImageTk 
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.color import label2rgb
from numpy import array
import numpy as np
import tkinter as tk 
from tkinter import *
import PIL
from math import sqrt
def Contenedor(img, img_binary):
	arr_binary = array(img_binary)
	arr_closed = closing(arr_binary, square(3))
	arr_labeled = label(arr_closed)
	regiones = regionprops(arr_labeled)
	_contenedor = None
	for region in regiones:
		# if region.area < area_min_contenedor: continue
		_contenedor = region if _contenedor==None or _contenedor.area < region.area else _contenedor
	b = _contenedor.bbox if _contenedor != None else None
	if b != None :
		xa = b[1] - 2 if b[1] - 2 >= 0 else 0
		ya = b[0] - 2 if b[0] - 2 >= 0 else 0
		xb = b[3] + 2 if b[3] + 2 <= img.size[0] else img.size[0]
		yb = b[2] + 2 if b[2] + 2 <= img.size[1] else img.size[1]
	return  img.crop([xa,ya,xb,yb] if _contenedor != None else [0,0,img.size[1],img.size[0]])
def Regiones(img_binary, ventana=9):
	# print("Regiones")
	# ventana = int(sqrt(ventana))
	# ventana += 1 if ventana % 2 == 0 else 0
	ventana = 3
	arr_binary = array(img_binary)
	arr_closed = closing(arr_binary, square(ventana))
	arr_labeled = label(arr_closed)
	return regionprops(arr_labeled)
def Mediciones(regiones,area_min):
	media = -1
	std = -1
	while media == -1 or media > area_min + std*3:#std > media * .5:
		areas = []
		validos = []
		for region in regiones:
			if (media == -1) or region.area > media - std*.5 and region.area < media + std*.5:
				areas.append(region.area)
				validos.append(region)
		media = np.mean(areas)
		std = np.std(areas)
		print("Mediciones",media, std)
	validos = []
	for region in regiones:
		if region.area > media - std and region.area < media + std and region.area > area_min:
			validos.append(region.label)
	return media, std, validos
current = 0
def CheckRestos(imagen_posta, regiones, media, std):
	cantidades = []
	for region in regiones:
		c = region.area / media
		cantidades.append(int(c))
	def move(delta):
	    global current
	    cantidades[current] = int(v.get()) if str.isdigit(v.get()) else 0
	    if not (0 <= current + delta < len(regiones)):
	        return
	    current += delta
	    a,b,c,d = regiones[current].bbox
	    image = imagen_posta.crop([b-10,a-10,d+10,c+10])
	    data_img = regiones[current].image
	    pixeles = image.load()
	    for x in range(len(data_img)):
	    	for y in range(len(data_img[x])):
	    		if data_img[x][y]:
	    			_x = x + 10
	    			_y = y + 10
	    			pixeles[_y,_x] = (pixeles[_y,_x][0],pixeles[_y,_x][1],255)
	    # draw = ImageDraw.Draw(image)
	    # draw.rectangle([10,10,d-b+10,c-a + 10], fill=None, outline='red')
	    # del draw
	    image = image.resize((image.size[0]*3,image.size[1]*3))
	    # image = image.resize(((b-a),(d-c)))
	    photo = ImageTk.PhotoImage(image)
	    label['text'] = str(current + 1) + " de " + str(len(regiones))
	    label['image'] = photo
	    label.photo = photo
	    v.set(cantidades[current])
	def escribir(delta):
		global current
		cantidades[current] = int(v.get()) if str.isdigit(v.get()) else 0

	root = tk.Tk()
	frame = tk.Frame(root)
	frame.pack()
	v = StringVar()
	
	entrada = tk.Entry(root, textvariable=v)
	entrada.bind("<Key>", escribir)
	entrada.pack()
	tk.Button(frame, text='Anterior', command=lambda: move(-1)).pack(side=tk.LEFT)
	tk.Button(frame, text='Siguiente', command=lambda: move(+1)).pack(side=tk.LEFT)
	tk.Button(frame, text='Listo', command=root.quit).pack(side=tk.LEFT)

	label = tk.Label(root, compound=tk.TOP)
	label.pack()
	move(0)
	root.mainloop()
	return sum(cantidades)

def CheckRestos2(imagen_posta, regiones, media, std):
	cantidades = []
	for region in regiones:
		c = region.area / media
		cantidades.append([region.label, int(c)])
	def move(delta):
	    global current
	    cantidades[current][1] = int(v.get()) if str.isdigit(v.get()) else 0
	    if not (0 <= current + delta < len(regiones)):
	        return
	    current += delta
	    a,b,c,d = regiones[current].bbox
	    image = imagen_posta.crop([b-10,a-10,d+10,c+10])
	    data_img = regiones[current].image
	    pixeles = image.load()
	    for x in range(len(data_img)):
	    	for y in range(len(data_img[x])):
	    		if data_img[x][y]:
	    			_x = x + 10
	    			_y = y + 10
	    			pixeles[_y,_x] = (pixeles[_y,_x][0],pixeles[_y,_x][1],255)
	    image = image.resize((image.size[0]*3,image.size[1]*3))
	    photo = ImageTk.PhotoImage(image)
	    label['text'] = str(current + 1) + " de " + str(len(regiones))
	    label['image'] = photo
	    label.photo = photo
	    v.set(cantidades[current][1])
	def escribir(delta):
		global current
		cantidades[current][1] = int(v.get()) if str.isdigit(v.get()) else 0

	root = tk.Tk()
	frame = tk.Frame(root)
	frame.pack()
	v = StringVar()
	
	entrada = tk.Entry(root, textvariable=v)
	entrada.bind("<Key>", escribir)
	entrada.pack()
	tk.Button(frame, text='Anterior', command=lambda: move(-1)).pack(side=tk.LEFT)
	tk.Button(frame, text='Siguiente', command=lambda: move(+1)).pack(side=tk.LEFT)
	tk.Button(frame, text='Listo', command=root.destroy).pack(side=tk.LEFT)

	label = tk.Label(root, compound=tk.TOP)
	label.pack()
	move(0)
	root.mainloop()
	return cantidades