from PIL import Image, ImageDraw, ImageOps,ImageFilter
import funciones as fn
img = Image.open("../imagen/IMG_20180118_084215.jpg")
tamfilter = 3
# img = ImageOps.equalize(img)
# self.img = ImageOps.autocontrast(self.img)
img = img.filter(ImageFilter.RankFilter(tamfilter, int(tamfilter*tamfilter/2)))
# Escalar
size = img.size
tam = 1600
img = img.resize((tam, int(size[1] * tam / size[0]))) if size[0] > size[1] else  img.resize((int(size[0] * tam / size[1]),tam))
img_gray = img.convert('L')
img_binary = img_gray.point(lambda p: p < 100 and 255)
regiones = fn.Regiones(img_binary)
media, std, validos = fn.Mediciones(regiones)
print("contadas", len(validos))
print("calculando restos")
restos = [region for i,region in enumerate(regiones) if i not in validos and region.area > media - std * 3]
print("restos", len(restos))
total = len(validos) + fn.CheckRestos(img,restos,media,std)
print("total",total)
