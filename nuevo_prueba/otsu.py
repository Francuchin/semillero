import matplotlib.pyplot as plt
# from skimage import data
from PIL import Image
from skimage import filters
from skimage import io
from skimage import exposure
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
import matplotlib.patches as patches

file_image = "../imagen/IMG_20180118_084215.jpg"
img = Image.open(file_image)

im = io.imread(file_image, 'L')
# val = filters.threshold_otsu(im)
val = filters.threshold_isodata(im)

arr_binary = im < val
# arr_closed = closing(arr_binary, square(3))
# arr_labeled = label(arr_closed)
# regiones = regionprops(arr_labeled)

# fig, ax = plt.subplots()
# plt.imshow(im, cmap='gray' )
# for region in regiones:
# 	b = region.bbox
# 	xa = b[1] - 2 if b[1] - 2 >= 0 else 0
# 	ya = b[0] - 2 if b[0] - 2 >= 0 else 0
# 	xb = b[3] + 2 if b[3] + 2 <= img.size[0] else img.size[0]
# 	yb = b[2] + 2 if b[2] + 2 <= img.size[1] else img.size[1]
# 	ax.add_patch(patches.Rectangle(
# 		        (xa, ya),
# 		        xb - xa,
# 		        yb - ya,
# 		        fill=False,
# 		        edgecolor='blue',
# 		        alpha=.4
# 		    ))
# plt.show()



hist, bins_center = exposure.histogram(im)

plt.figure(figsize=(9, 4))
plt.subplot(131)
plt.imshow(im, cmap='gray', interpolation='nearest')
plt.axis('off')
plt.subplot(132)
plt.plot(bins_center, hist, lw=2)
plt.axvline(val, color='k', ls='--')
plt.axis('off')
plt.subplot(133)
binaria = im < val
plt.imshow(binaria, cmap='gray', interpolation='nearest')
plt.axis('off')
plt.tight_layout()
plt.show()
