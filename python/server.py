from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import cgi
import time
from semillas import contar
from image import *
from io import BytesIO
def tuplify(listything):
    if isinstance(listything, list): return tuple(map(tuplify, listything))
    if isinstance(listything, dict): return {k:tuplify(v) for k,v in listything.items()}
    return listything
def regionTojson(region):
    return {
        "area": str(region.area),
        "bbox": tuplify(region.bbox),
        "centroid": tuplify(region.centroid)
    }

class StoreHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['content-length'])
        if length > 10000000:
            read = 0
            while read < length:
                read += len(self.rfile.read(min(66556, length - read)))
            self.respond("file to big")
            return
        else:
            form = cgi.FieldStorage(fp=self.rfile,headers=self.headers,environ={'REQUEST_METHOD': 'POST'})
            filename = form['file'].filename
            x = int(form['x'].value)
            y = int(form['y'].value)
            w = int(form['w'].value)
            h = int(form['h'].value)
            print("pito")
            #self.muestras = {0:(50,50,550,900)}
            self.muestras = {0:(x,y,w,h)}
            data = form['file'].file.read()
            open("/tmp/%s"%filename, "wb").write(data)
            self.ruta = "/tmp/%s"%filename # 742 semillas contadas a mano en 20 minutos
            self.img = get_imagen_pil(self.ruta)
            self.img_ski = get_imagen_ski(self.ruta)
            self.prom, self.std = 1, 0
            self.umbral_otsu = 0.5
            self.regiones = self.seguras = self.inseguras = []
            p = []
            s = []
            u = []
            for i in dict(self.muestras):
                _p,_s = self.GetArea_mean_std(self.muestras[i])
                u.append(umbral_otsu(np.asarray(self.img.crop(self.muestras[i]).convert('L'))))
                p.append(_p)
                s.append(_s)
            self.prom, self.std = np.mean(p) , np.mean(s)
            self.umbral_otsu = np.mean(u)
            self.regiones = otsu(self.img_ski,self.umbral_otsu)
            self.seguras, self.inseguras = contar(self.regiones, self.prom, self.std)
            self.inseguras = sorted(self.inseguras, key=lambda x: x.area, reverse=False)

            datos={
                "seguras": [regionTojson(region) for region in self.seguras ] , 
                "inseguras":[regionTojson(region) for region in self.inseguras ] 
                }
            json_response=json.dumps(datos, ensure_ascii=False)
            self.respond(json_response,"application/json")

    def GetArea_mean_std(self, muestra):
        img_binary = np.asarray(self.img.crop(muestra).convert('L'))
        regiones = otsu(img_binary)
        areas = [r.area for r in regiones]
        return np.mean(areas), np.std(areas)
    def do_GET(self):
        response = """
        <html><body>
        <form enctype="multipart/form-data" method="post">
        <p>File: <input type="file" name="file"></p>
        <select name="estudio" > 
        <option value="1">Semillas</option>
        <option value="2">Perros</option>
        </select>
        <p><input type="submit" value="Upload"></p>
        </form>
        </body></html>
        """        

        self.respond(response)

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")

    def respond(self, response, content="text/html", status=200):
        self.send_response(status)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Content-type", content)
        self.end_headers()
        self.wfile.write(bytes(response, "utf-8"))


hostName = '0.0.0.0'
hostPort = 8080

myServer = HTTPServer((hostName, hostPort), StoreHandler)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))