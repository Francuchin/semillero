from correcciones import FrCorrecciones, FrResultados
from muestras import FrMuestras

from semillas import contar
from cargando import FrCarga
from image import *

import threading, queue

from tkinter import *
from tkinter.filedialog import askopenfilename

class App(Tk):

	def __init__(self, *args, **kwargs):
		Tk.__init__(self, *args, **kwargs)
		archivo = askopenfilename(
			initialdir = ".",
			filetypes =(("Imágenes", "*.jpg"),("All Files","*.*")),
			title = "Seleccionar archivo") or "semillas.jpg"
		self.title("Semillero")
		self.state('zoomed')
		# self.configure(background='black')
		self.ruta = archivo # 742 semillas contadas a mano en 20 minutos
		self.img = get_imagen_pil(self.ruta)
		self.img_ski = get_imagen_ski(self.ruta)
		self.frames = {}
		self.prom, self.std = 1, 0
		self.umbral_otsu = 0.5
		self.regiones = self.seguras = self.inseguras = []

		for F in (FrMuestras, FrCorrecciones, FrResultados, FrCarga):
			page_name = F.__name__
			frame = F(parent=self, controller=self)
			self.frames[page_name] = frame
			frame.grid(row=0, column=0, sticky="nsew")
		self.show_frame("FrMuestras")

	def show_frame(self, page_name):
		frame = self.frames[page_name]
		frame.tkraise()

	def analizar(self):
		self.queue = queue.Queue()
		self.bl()
		t1 = threading.Thread(name='segmentacion', target=self.segmentacion)
		t1.daemon = True
		t1.start()
	# Bloqueo
	def bl(self):
		try:
			msg = self.queue.get(0)
			self.title(msg)
			if(str(msg)=="Listo"):
				self.frames["FrCorrecciones"].cargar()
				self.show_frame("FrCorrecciones")
			else:
				self.show_frame("FrCarga")
				self.frames["FrCarga"].texto(msg)
				self.after(100, self.bl)
		except queue.Empty:
			self.show_frame("FrCarga")
			self.after(100, self.bl)

	def segmentacion(self):
		self.queue.put("Iniciando Segmentacion")
		self.regiones = otsu(self.img_ski,self.umbral_otsu, self.queue)
		self.queue.put("Clasificando")
		self.seguras, self.inseguras = contar(self.regiones, self.prom, self.std)
		self.queue.put("Ordenando Resultados")
		self.inseguras = sorted(self.inseguras, key=lambda x: x.area, reverse=False)
		self.queue.put("Listo")

if __name__ == "__main__":
    app = App()
    app.mainloop()
    