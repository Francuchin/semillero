# from PIL import Image
# import matplotlib.pyplot as plt

# image = Image.open("imagen/50.jpg").convert('L')
# histogram = image.histogram()
# for i in range(len(histogram)):
# 	color = ('#%02x%02x%02x' % (i,i,i))
# 	plt.bar(i, histogram[i], color=color, edgecolor=color)
# plt.show()
from PIL import Image, ImageFilter
import numpy as np

im = Image.open('imagen/50.jpg')
im = im.convert('L')

data = np.array(im)
a = data.T
white_areas = (a > 60)
data[white_areas.T] = (255) 

size = 15
im = im.filter(ImageFilter.RankFilter(size, int(size*size/2)))

im = Image.fromarray(data)
im.show()