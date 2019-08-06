import tkinter
from tkinter import *
from PIL import Image, ImageTk
import ctypes
import numpy as np
import funciones as fn
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

rectx0 = rectx1 = recty0 = recty1 = 0
rectid = None
move = False

def TomarMuestra(img_orig):
	tk = Tk()
	tk.title("Seleccionando Muestras")
	tk.attributes("-fullscreen", True)

	tk.columnconfigure(1, weight=1)
	tk.columnconfigure(3, pad=7)
	tk.rowconfigure(3, weight=1)
	tk.rowconfigure(5, pad=7)

	size =  int(screensize[0]/2), screensize[1]
	canvas = Canvas(tk,width = int(screensize[0]/2), height = screensize[1])
	canvas.grid(row=0, column=0)
	img = img_orig
	original_size = img_orig.size
	img = img.resize(size)
	aspecto = (original_size[0]/img.size[0],original_size[1]/img.size[1])
	photo = ImageTk.PhotoImage(img)
	canvas.create_image(0,0,anchor=NW, image=photo)

	lista = Listbox(width=50, height=30)
	lista.grid(row=0, column=1, sticky="NW")
	frame1 = Frame(tk)
	frame1.grid(row=0,column=2)
	ver = Button(frame1,text="Ver Muestra", command = lambda: ver(lista))
	ver.pack()
	delete = Button(frame1,text="Eliminar Muestra", command = lambda: deletefunc(lista))
	delete.pack()
	listo = Button(frame1,text="Listo", command=tk.destroy)
	listo.pack()

	muestras = {}

	def ver(l):
		selection = l.curselection()
		if selection:
			if l.get(ACTIVE):
				item = l.get(ACTIVE)[0]
				rect = muestras.get(item)
				img = img_orig.crop(rect)
				_tk = Tk()
				_tk.title("Ver Muestra")
				_canvas = Canvas(_tk,width = img.size[0], height = img.size[1])
				_photo = ImageTk.PhotoImage(img, master=_canvas,width = img.size[0], height = img.size[1])
				_canvas.create_image(0,0,anchor=NW, image=_photo)
				_canvas.grid(row=0, column=0)
				_tk.mainloop()
	def deletefunc(l):
		selection = l.curselection()
		if selection:
			if l.get(ACTIVE):
				item = l.get(ACTIVE)[0]
				muestras.pop(item)
				l.delete(selection[0])
				canvas.delete(item)
	def startRect(event):
		global move, rectx0, rectx1, recty0, recty1, rectid
		move = True
		rectx0 = canvas.canvasx(event.x)
		recty0 = canvas.canvasy(event.y)
		rect = canvas.create_rectangle( rectx0, recty0, rectx0, recty0, fill=None)
		rectid = canvas.find_closest(rectx0, recty0, halo=2)
		# print('rectangulo {0} inicia en {1} {2} {3} {4} '.format(rect, rectx0, recty0, rectx0,recty0))

	def movingRect(event):
		global move, rectx0, rectx1, recty0, recty1, rectid
		if move: 
			rectx1 = canvas.canvasx(event.x)
			recty1 = canvas.canvasy(event.y)
			canvas.coords(rectid, rectx0, recty0,rectx1, recty1)
			# print('escalando rectangulo', rectx1, recty1)

	def stopRect(event):
		global move, rectx0, rectx1, recty0, recty1, rectid
		move = False
		rectx1 = canvas.canvasx(event.x)
		recty1 = canvas.canvasy(event.y) 
		canvas.coords(rectid, rectx0, recty0, rectx1, recty1)
		a,b,c,d = rectx0, recty0, rectx1, recty1
		if a > c: a,c=c,a
		if b > d: d,b=b,d
		muestras.update({rectid[0]:[int(a*aspecto[0]), int(b*aspecto[1]), int(c*aspecto[0]), int(d*aspecto[1]) ]})
		lista.insert(0, rectid)
		# print('Termina rectangulo')

	canvas.bind( "<Button-1>", startRect )
	canvas.bind( "<ButtonRelease-1>", stopRect )
	canvas.bind( "<Motion>", movingRect )
	mainloop()
	return muestras
def GetBajos(canal):
	c = []
	std = np.std(canal)
	minimo = min(canal)
	for v in canal:
		if(v < minimo + std * 3):
			c.append(v)
	return c
	# return max(canal) - min(canal) - std * 3
def GetColor(img_orig,muestra):
	crop = img_orig.crop(muestra)
	size = crop.size
	pixeles = crop.load()
	R,G,B = [],[],[]
	for x in range(size[1]):
		for y in range(size[0]):
			R.append(pixeles[y,x][0])
			G.append(pixeles[y,x][1])
			B.append(pixeles[y,x][2])
	_R,_G,_B = GetBajos(R),GetBajos(G),GetBajos(B)
	return int(np.mean(_R)),int(np.mean(_G)),int(np.mean(_B))
def GetArea(img_orig,muestra, umbral):
	mask_R = [255 if 0 <= x <= umbral[0] else 0 for x in range(0, 256)]
	mask_G = [255 if 0 <= x <= umbral[1] else 0 for x in range(0, 256)]
	mask_B = [255 if 0 <= x <= umbral[2] else 0 for x in range(0, 256)]
	img_binary = img_orig.crop(muestra).point(mask_R+mask_G+mask_B).convert('L').point([0]*255+[255])
	regiones = fn.Regiones(img_binary)
	return np.mean([r.area for r in regiones])

def Muestra(img_orig):
	muestras = TomarMuestra(img_orig)
	resultados = []
	for i in muestras:
		umbral = GetColor(img_orig,muestras[i])
		resultados.append([umbral, GetArea(img_orig,muestras[i], umbral)])
	return resultados
# print(Muestra(image_file = "../imagen/IMG_20180118_084153.jpg"))