import numpy as np

error = 1

def tuplify(listything):
    if isinstance(listything, list): return tuple(map(tuplify, listything))
    if isinstance(listything, dict): return {k:tuplify(v) for k,v in listything.items()}
    return listything

def getpromstd(regiones):
	areas = [region.area for region in regiones]
	return np.mean(areas), np.std(areas)
def regionTojson(region,cantidad):
    return {
        "area": str(region.area),
        "cantidad": str(cantidad),
        "bbox": tuplify(region.bbox),
        "centroid": tuplify(region.centroid),
        "convex_image":region.convex_image.tolist()
    }
def contar(regiones, area_promedio, area_std):
	seguro = []
	inseguro = []
	area_promedio, area_std = getpromstd(regiones)
	total = 0
	for region in regiones:
		if region.area < area_promedio + (area_std * error) and region.area > area_promedio - (area_std * error):
			total = total + 1;
			seguro.append(regionTojson(region,1))
		else:
			if region.area > area_promedio - 2 * area_std:
				cantidad = region.area / area_promedio
				arriba = (int(cantidad) * area_promedio) + area_std
				abajo  = (int(cantidad) * area_promedio) - area_std
				if abs(arriba - region.area) > abs(region.area - abajo):
					cantidad = (region.area - area_std) / area_promedio
				else:
					cantidad = (region.area + area_std) / area_promedio
				total = total + int(cantidad)
				inseguro.append(regionTojson(region,cantidad))
	return seguro, inseguro, area_promedio, area_std, total