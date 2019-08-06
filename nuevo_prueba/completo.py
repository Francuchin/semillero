import tkinter
from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk, ImageDraw
import ctypes
import numpy as np
import funciones as fn

file_image = "../imagen/IMG_20180118_084215.jpg"

UMBRAL = [(0,70), (0,150), (0,70)]

im = Image.open(file_image)

def Actualizar():
	barraestado.config(text="Analizando") 
	global im
	global photo
	global canvas
	global item_image	 
	im = Image.open(file_image)
	im = im.resize((600,400))
	photo = ImageTk.PhotoImage(im)
	canvas.itemconfigure(item_image, image=photo)
	barraestado.config(text="Listo")  

def archivo():
	barraestado.config(text="Cargando imagen")  
	global file_image
	file_image = askopenfilename(
		initialdir = ".",
		filetypes =(("Imágenes", "*.jpg"),("All Files","*.*")),
		title = "Seleccionar archivo")
	if file_image != "":
		Actualizar()
	else:
		barraestado.config(text="Carga cancelada") 


tk = Tk()
tk.title("Conteo de semillas")

# tk.iconbitmap('../py.ico')
menubarra = Menu(tk)

menuarchivo = Menu(menubarra, tearoff=0)

menuarchivo.add_command(label="Abrir", command=archivo)
menuarchivo.add_command(label="Actualizar", command=Actualizar)
menuarchivo.add_separator()
menuarchivo.add_command(label="Salir", command=tk.quit)
menubarra.add_cascade(label="Archivo", menu=menuarchivo)

tk.config(menu=menubarra)

frame0 = Frame(tk)
frame0.pack(fill="both", expand=True)

canvas = Canvas(frame0,width = 600, height = 400)
canvas.pack(fill="both", expand=True)
im = im.resize((600,400))
photo = ImageTk.PhotoImage(im)
item_image = canvas.create_image(0,0,anchor=NW, image=photo)

barraestado = Label(tk, bd=1, relief=SUNKEN, anchor=W)
barraestado.pack(side=BOTTOM,fill=X)   
mainloop()