from PIL import Image, ImageDraw, ImageOps,ImageFilter
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import funciones as fn
print("1")
img = Image.open("../imagen/IMG_20180118_084215.jpg")
# Escalar
size = img.size
tam = 1600
img = img.resize((tam, int(size[1] * tam / size[0]))) if size[0] > size[1] else  img.resize((int(size[0] * tam / size[1]),tam))
print("2")
img_gray = img.convert('L')
# Pre procesamiento
# img = img.filter(ImageFilter.GaussianBlur())
# img = img.filter(ImageFilter.UnsharpMask(4))
# tamfilter = 3
# img = img.filter(ImageFilter.RankFilter(tamfilter, int(tamfilter*tamfilter/2)))
# Binario
img_binary = img_gray.point(lambda p: p < 100 and 255)
print("3")
# img_binary.show()
regiones = fn.Regiones(img_binary)
media, std, validos = fn.Mediciones(regiones,180)
print("4")
#posprocesamiento
# img_binary = img_binary.filter(ImageFilter.MaxFilter(3))
# img_binary = img_binary.filter(ImageFilter.MinFilter(3)) 
# img_binary.show()
# Fin
print("contadas", len(validos))
# fig, ax = plt.subplots()
# plt.imshow(img)
# for p in [
#     [patches.Rectangle(
#         (r.bbox[1], r.bbox[0]),
#         r.bbox[3] - r.bbox[1],
#         r.bbox[2] - r.bbox[0],
#         fill=False,
#         edgecolor='blue',
#         alpha=.4
#     ), r.centroid] for r in validos]: 
#     ax.add_patch(p[0])
print("calculando restos")
restos = [region for i,region in enumerate(regiones) if i not in validos and region.area > media - std * 3]
# restos = []
# for region in regiones:
# 	if region not in validos and region.area > media - std * 3:
# 		restos.append(region)
print("restos", len(restos))
total = len(validos) + fn.evaluar(img,restos,media,std)
print("total",total)
# for p in [
#     [patches.Rectangle(
#         (r.bbox[1], r.bbox[0]),
#         r.bbox[3] - r.bbox[1],
#         r.bbox[2] - r.bbox[0],
#         fill=False,
#         edgecolor='red',
#         alpha=.4
#     ), r.centroid] for r in restos]: 
#     ax.add_patch(p[0])
# plt.show()
# fn.ventana(img)