import numpy as np

error = 1

def getpromstd(regiones):
	areas = [region.area for region in regiones]
	return np.mean(areas), np.std(areas)

def contar(regiones, area_promedio, area_std):
	seguro = []
	inseguro = []
	area_promedio, area_std = getpromstd(regiones)
	for region in regiones:
		if region.area < area_promedio + (area_std * error) and region.area > area_promedio - (area_std * error):
			seguro.append(region)
		else:
			if region.area > area_promedio - 2 * area_std:
				cantidad = region.area / area_promedio
				arriba = (int(cantidad) * area_promedio) + area_std
				abajo  = (int(cantidad) * area_promedio) - area_std
				if abs(arriba - region.area) > abs(region.area - abajo):
					cantidad = (region.area - area_std) / area_promedio
				else:
					cantidad = (region.area + area_std) / area_promedio
				region.cantidad = cantidad
				inseguro.append(region)
	return seguro, inseguro