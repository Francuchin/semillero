from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import json
import cgi

from semillas import contar
from image import *

class StoreHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print self.headers['content-length']
        length = int(self.headers['content-length'])
        print length
        if length > 10000000:
            print "file to big"
            read = 0
            while read < length:
                read += len(self.rfile.read(min(66556, length - read)))
            self.respond("file to big")
            return
        else:
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                         'CONTENT_TYPE':self.headers['Content-Type'],
                         })
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
            p = []
            s = []
            u = []
            for i in dict(self.muestras):
            	_p,_s = self.GetArea_mean_std(self.muestras[i])
            	u.append(umbral_otsu(np.asarray(self.img_orig.crop(self.muestras[i]).convert('L'))))
            	p.append(_p)
            	s.append(_s)
            self.prom, self.std = np.mean(p) , np.mean(s)
            self.umbral_otsu = np.mean(u)
            self.regiones = otsu(self.img_ski,self.umbral_otsu)
            self.seguras, self.inseguras = contar(self.regiones, self.prom, self.std)
            self.inseguras = sorted(self.inseguras, key=lambda x: x.area, reverse=False)
            self.respond(json.dumps({
            	"estudio":estudio,
            	"seguras":self.seguras, 
            	"inseguras":self.inseguras
            	}))

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

    def respond(self, response, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(response))
        self.end_headers()
        self.wfile.write(response)  


server = HTTPServer(('', 8080), StoreHandler)
server.serve_forever()