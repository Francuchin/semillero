# import the necessary packages
from shapeDetector import ShapeDetector
import imutils
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import time
# load the image and resize it to a smaller factor so that
# the shapes can be approximated better
image = cv2.imread('imagen/IMG_20180118_084416.jpg')
brillo = 20
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# inicio = time.clock()
# for x in range(0, len(hsv)):
#     for y in range(0, len(hsv[0])):
#     	if (hsv[x, y][2] + brillo <= 255):
#     		hsv[x, y][2] += brillo
#     	else:
#     		hsv[x, y][2] = 255
# fin = time.clock()
# 5.70180040049446e-07 109.38281716834908 109.38281659816904
inicio = time.clock()
hsv[:,:,2] += brillo
fin = time.clock()
# 1.710540120148338e-06 0.010338504486176556 0.010336793946056407
print (inicio, fin, fin - inicio)
image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

# resized = imutils.resize(image, width=1024)
# convert the resized image to grayscale, blur it slightly,
# and threshold it
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
# contraste = cv2.equalizeHist(blurred)
thresh = cv2.threshold(blurred, 65, 255, cv2.THRESH_BINARY)[1]
thresh = cv2.bitwise_not(thresh)
# find contours in the thresholded image and initialize the
# shape detector
cnts = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
sd = ShapeDetector()
# loop over the contours

semillas = []

for i,c in enumerate(cnts):
	# compute the center of the contour, then detect the name of the
	# shape using only the contour
	M = cv2.moments(c)
	if M["m00"] == 0: continue
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])
	shape = sd.detect(c)
	# multiply the contour (x, y)-coordinates by the resize ratio,
	# then draw the contours and the name of the shape on the image
	c = c.astype("int")
	# cv2.drawContours(image, [c], -1, (0, 255, 0), 1)
	# cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 1)
	semillas.append([i,cX,cY,c, shape])
from matplotlib.patches import Polygon
import randomcolor
fig, ax = plt.subplots()
rand_color = randomcolor.RandomColor()

for semilla in semillas:
	puntos = [ [ p[0][0],p[0][1] ] for p in semilla[3] ]
	ax.add_patch(Polygon(puntos, False, color=rand_color.generate()[0]))
	x = np.mean([p[0] for p in puntos])
	y = np.mean([p[1] for p in puntos])
	plt.plot(x, y, 'ro')
plt.imshow(image)
plt.show()
# plt.savefig("wea.jpg")