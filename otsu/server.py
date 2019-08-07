from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import cgi
import time
from semillas import contar
from image import *
from io import BytesIO

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
            estudio = form['estudio'].value
            muestras = [(0,0,250,250)]#form['muestras'].value
            data = form['file'].file.read()
            open("/tmp/%s"%filename, "wb").write(data)
            self.ruta = "/tmp/%s"%filename # 742 semillas contadas a mano en 20 minutos
            self.img = get_imagen_pil(self.ruta)
            self.img_ski = get_imagen_ski(self.ruta)
            self.prom, self.std = 1, 0
            self.umbral_otsu = 0.5
            self.regiones = self.seguras = self.inseguras = []

            datos={"estudio":estudio}
            json_response=json.dumps(datos, ensure_ascii=False)
            self.respond(json_response,"application/json")

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

    def respond(self, response, content="text/html", status=200):
        self.send_response(status)
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