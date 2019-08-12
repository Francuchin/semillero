import tkinter as tk 
from PIL import ImageTk,ImageDraw 
from tkinter import *
import ctypes

current = 0
borde = 30
def GetEscala():
	user32 = ctypes.windll.user32
	W,H = user32.GetSystemMetrics(0) / 1.3, user32.GetSystemMetrics(1) / 1.3
	return int(H * H / W), int(H)

def recorteCentrado(y,x,w,h):
	L = T = 0
	R = w
	B = h
	_w = w/5
	_h = h/5
	if x - _w < 0:
		L = 0
		R = _w
	else:
		if x + _w > w:
			L = w - _w
			R = w
		else:
			L = x - (_w/2)
			R = x + (_w/2)
	if y - _h < 0:
		T = 0
		B = _h
	else:
		if y + _h > h:
			T = h - _h
			B = h
		else:
			T = y - (_h/2)
			B = y + (_h/2)
	return int(L), int(T), int(R), int(B)

class FrCorrecciones(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.parent = parent
		self.controller = controller
		self.regiones_inseguras = self.controller.inseguras
		self.imagen_posta = self.controller.img
		self.cantidades = [int(round(region.cantidad)) for region in self.regiones_inseguras ]		
		self.current = 0
		self.v = StringVar()
		frame = Frame(self)
		frame.pack()
		self.entrada = Entry(self, textvariable=self.v)
		self.entrada.bind("<Key>", self.escribir)
		self.entrada.pack()
		Button(frame, text='Anterior', command=lambda: self.move(-1)).pack(side=LEFT)
		Button(frame, text='Siguiente', command=lambda: self.move(+1)).pack(side=LEFT)
		# Button(frame, text='Listo', command=root.quit).pack(side=tk.LEFT)
		self.contenedor_imagenes = Frame(self)
		self.contenedor_imagenes.pack(side=TOP)

		self.imagen_lejos = Label(self.contenedor_imagenes, compound=TOP)
		self.imagen_lejos.pack(side=LEFT)
		self.imagen_cerca = Label(self.contenedor_imagenes, compound=TOP)
		self.imagen_cerca.pack(side=LEFT)
		self.label_total = Label(self.contenedor_imagenes, compound=TOP)
		self.label_total.pack(side=LEFT)

	def cargar(self):
		self.imagen_posta = self.controller.img
		self.regiones_inseguras = self.controller.inseguras
		self.cantidades = [int(round(region.cantidad)) for region in self.regiones_inseguras ]
		self.current = 0
		self.focus_force()
		self.move(0)
		# self.controller.overrideredirect(True)
		
	def move(self, delta):
	    W,H = GetEscala()
	    self.entrada.select_range(0, END)
	    self.entrada.focus()
	    if(delta != 0):
	    	self.cantidades[self.current] = int(self.v.get()) if str.isdigit(self.v.get()) else 0
	    if not (0 <= self.current + delta < len(self.regiones_inseguras)):
	        return
	    self.current += delta
	    a,b,c,d = self.regiones_inseguras[self.current].bbox
	    ####
	    centro=self.regiones_inseguras[self.current].centroid
	    L,T,R,B=recorteCentrado(centro[0],centro[1], self.imagen_posta.size[0], self.imagen_posta.size[1])
	    img_lejos = self.imagen_posta.copy()
	    draw = ImageDraw.Draw(img_lejos)
	    draw.rectangle([b-borde,a-borde,d+borde,c+borde], outline=128)
	    del draw	    
	    img_lejos = img_lejos.crop([L,T,R,B])
	    img_lejos = img_lejos.resize((W,H))
	    photo_lejos = ImageTk.PhotoImage(img_lejos)
	    self.imagen_lejos['text'] = "zoom" 
	    self.imagen_lejos['image'] = photo_lejos
	    self.imagen_lejos.photo = photo_lejos
	    del img_lejos
	    ####
	    image = self.imagen_posta.crop([b-borde,a-borde,d+borde,c+borde])
	    data_img = self.regiones_inseguras[self.current].image
	    pixeles = image.load()
	    for x in range(len(data_img)):
	    	for y in range(len(data_img[x])):
	    		if data_img[x][y]:
	    			_x = x + borde
	    			_y = y + borde
	    			pixeles[_y,_x] = (pixeles[_y,_x][0],pixeles[_y,_x][1],255)
	    image = image.resize((W,H))
	    photo = ImageTk.PhotoImage(image)
	    self.imagen_cerca['text'] = str(self.current + 1) + " de " + str(len(self.regiones_inseguras))
	    self.imagen_cerca['image'] = photo
	    self.imagen_cerca.photo = photo
	    self.v.set(self.cantidades[self.current])
	    self.actualizarCantidad()

	def actualizarCantidad(self):
		self.label_total['text'] = str(len(self.controller.seguras) + sum(self.cantidades))

	def escribir(self, delta):
		self.cantidades[self.current] = int(self.v.get()) if str.isdigit(self.v.get()) else 0
		self.actualizarCantidad()

class FrResultados(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.parent = parent
		self.controller = controller
