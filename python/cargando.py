from tkinter import *

ind = 0
top = frames = None 
fin = 0

class FrCarga(Frame):
	
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.frames = [PhotoImage(file="carga.gif",format = 'gif -index %i' %(i)) for i in range(12)]
		self.frame1 = Frame(self)
		self.frame1.pack(fill="x")
		self.label = Label(self.frame1, compound=TOP)
		self.label['text'] = "cargando" 
		self.label.pack()
		self.after(80, self.actualizar, 0)

	def actualizar(self, ind):
		frame = self.frames[ind]
		ind = ind + 1 if (ind < len(self.frames) - 1 ) else 0
		self.label.configure(image=frame)
		self.after(80, self.actualizar, ind)
	def texto(self, texto):
		self.label['text'] = texto