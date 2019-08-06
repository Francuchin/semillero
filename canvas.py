from tkinter import *
from PIL import Image, ImageTk
# create the canvas, size in pixels
canvas = Canvas(width = 600, height = 400)
# pack the canvas into a frame/form
canvas.pack(expand=YES, fill=BOTH)
image_file = "imagen/50.jpg"
img = Image.open(image_file)
img = img.resize((600,400))
photo = ImageTk.PhotoImage(img)

canvas.create_image(0,0, image=photo)
# canvas.grid(row=0, column=0, sticky='nsew')

rectx0 = rectx1 = recty0 = recty1 = 0
rectid = None
move = False

def startRect(event):
	global move, rectx0, rectx1, recty0, recty1, rectid
	move = True
    #Translate mouse screen x0,y0 coordinates to canvas coordinates
	rectx0 = canvas.canvasx(event.x)
	recty0 = canvas.canvasy(event.y) 
    #Create rectangle
	rect = canvas.create_rectangle( rectx0, recty0, rectx0, recty0, fill=None)
    #Get rectangle's canvas object ID
	rectid = canvas.find_closest(rectx0, recty0, halo=2)
	print('Rectangle {0} started at {1} {2} {3} {4} '.
          format(rect, rectx0, recty0, rectx0,recty0))

def movingRect(event):
	global move, rectx0, rectx1, recty0, recty1, rectid
	if move: 
        #Translate mouse screen x1,y1 coordinates to canvas coordinates
		rectx1 = canvas.canvasx(event.x)
		recty1 = canvas.canvasy(event.y)
        #Modify rectangle x1, y1 coordinates
		canvas.coords(rectid, rectx0, recty0,rectx1, recty1)
		print('Rectangle x1, y1 = ', rectx1, recty1)

def stopRect(event):
	global move, rectx0, rectx1, recty0, recty1, rectid
	move = False
    #Translate mouse screen x1,y1 coordinates to canvas coordinates
	rectx1 = canvas.canvasx(event.x)
	recty1 = canvas.canvasy(event.y) 
    #Modify rectangle x1, y1 coordinates (final)
	canvas.coords(rectid, rectx0, recty0, rectx1, recty1)
	print('Rectangle ended')
canvas.bind( "<Button-1>", startRect )
canvas.bind( "<ButtonRelease-1>", stopRect )
canvas.bind( "<Motion>", movingRect )
# run it ...
mainloop()