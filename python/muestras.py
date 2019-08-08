from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import ctypes
import numpy as np
from image import *

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


class FrMuestras(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.parent = parent
		self.controller = controller
		self.rectx0 = self.rectx1 = self.recty0 = self.recty1 = 0
		self.rectid = None
		self.move = False
		self.size =  int(screensize[0]/2), screensize[1]
		self.canvas = Canvas(self,width = int(screensize[0]/2), height = screensize[1])
		self.canvas.grid(row=0, column=0)
		self.img_orig = self.controller.img
		self.img = self.img_orig
		self.original_size = self.img_orig.size
		self.img = self.img.resize(self.size)
		self.aspecto = (self.original_size[0]/self.img.size[0],self.original_size[1]/self.img.size[1])
		self.photo = ImageTk.PhotoImage(self.img)
		self.canvas.create_image(0,0,anchor=NW, image=self.photo)
		self.lista = Listbox(self,width=50, height=30)
		self.lista.grid(row=0, column=1, sticky="NW")
		self.frame1 = Frame(self)
		self.frame1.grid(row=0,column=2)
		self.verbtn = Button(self.frame1,text="Ver Muestra", command = lambda: self.ver(self.lista))
		self.verbtn.pack()
		self.delete = Button(self.frame1,text="Eliminar Muestra", command = lambda: self.deletefunc(self.lista))
		self.delete.pack()
		self.listo = Button(self.frame1,text="Listo", command = self.Listo)
		self.listo.pack()
		self.muestras = {}
		self.canvas.bind( "<Button-1>", self.startRect )
		self.canvas.bind( "<ButtonRelease-1>", self.stopRect )
		self.canvas.bind( "<Motion>", self.movingRect )

	def ver(self, l):
		# falata arreglar para que se vea en una miniatura en la misma pantalla
		selection = l.curselection()
		if selection:
			if l.get(ACTIVE):
				item = l.get(ACTIVE)[0]
				rect = self.muestras.get(item)
				img = self.img_orig.crop(rect)
				_tk = Tk()
				_tk.title("Ver Muestra")
				_canvas = Canvas(_tk,width = img.size[0], height = img.size[1])
				_photo = ImageTk.PhotoImage(img, master=_canvas,width = img.size[0], height = img.size[1])
				_canvas.create_image(0,0,anchor=NW, image=_photo)
				_canvas.grid(row=0, column=0)
				_tk.mainloop()
	def deletefunc(self, l):
		selection = l.curselection()
		if selection:
			if l.get(ACTIVE):
				item = l.get(ACTIVE)[0]
				self.muestras.pop(item)
				l.delete(selection[0])
				self.canvas.delete(item)
	def startRect(self, event):
		self.move = True
		self.rectx0 = self.canvas.canvasx(event.x)
		self.recty0 = self.canvas.canvasy(event.y)
		self.rect = self.canvas.create_rectangle( self.rectx0, self.recty0, self.rectx0, self.recty0, fill=None)
		self.rectid = self.canvas.find_closest(self.rectx0, self.recty0, halo=2)

	def movingRect(self, event):
		if self.move: 
			self.rectx1 = self.canvas.canvasx(event.x)
			self.recty1 = self.canvas.canvasy(event.y)
			self.canvas.coords(self.rectid, self.rectx0, self.recty0, self.rectx1, self.recty1)

	def stopRect(self, event):
		self.move = False
		self.rectx1 = self.canvas.canvasx(event.x)
		self.recty1 = self.canvas.canvasy(event.y) 
		self.canvas.coords(self.rectid, self.rectx0, self.recty0, self.rectx1, self.recty1)
		a,b,c,d = self.rectx0, self.recty0, self.rectx1, self.recty1
		if a > c: a,c=c,a
		if b > d: d,b=b,d
		self.muestras.update({self.rectid[0]:[int(a*self.aspecto[0]), int(b*self.aspecto[1]), int(c*self.aspecto[0]), int(d*self.aspecto[1]) ]})
		self.lista.insert(0, self.rectid)

	def GetArea_mean_std(self, muestra):
		img_binary = np.asarray(self.img_orig.crop(muestra).convert('L'))
		regiones = otsu(img_binary)
		areas = [r.area for r in regiones]
		return np.mean(areas), np.std(areas)

	def Listo(self):
		if (len(self.muestras)>4):
			p = []
			s = []
			u = []
			for i in dict(self.muestras):
				_p,_s = self.GetArea_mean_std(self.muestras[i])
				u.append(umbral_otsu(np.asarray(self.img_orig.crop(self.muestras[i]).convert('L'))))
				p.append(_p)
				s.append(_s)
			self.controller.prom, self.controller.std = np.mean(p) , np.mean(s)
			self.controller.umbral_otsu = np.mean(u)
			self.controller.analizar()
		else:
			messagebox.showerror("Error", "Se necesitan al menos 5 muestras")

def Resultado(self, res):
	tk = Tk()
	tk.title("Resultado")
	resultado = Label(tk, compound=TOP)
	resultado['text'] = str(res) + " Semillas contadas"
	resultado.pack(fill=BOTH, expand=1,pady=15,padx=70)
	Button(tk, text='Listo', command=tk.quit).pack(pady=20)
	mainloop()