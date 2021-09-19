import conf
import mimetypes
import os
from os import getcwd
from http.server import BaseHTTPRequestHandler, HTTPServer
from jinja2 import Environment, FileSystemLoader, select_autoescape
jinja = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)

 = "1.0.0"
print(conf.name + " " + conf.version)


class httpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        errorCode = 200
        if self.path == "/":
            filePath = os.path.join(os.getcwd(), conf.contentFolder + "/index.html")
        else:
            filePath = os.path.join(os.getcwd(), conf.contentFolder + self.path)
            if not os.path.isfile(filePath):
                errorCode = 404

        def detect(bytes): return bool(bytes.translate(None, bytearray(
            {7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})))
        self.send_response(errorCode)
        type = mimetypes.guess_type(self.path)
        if type == None:
            self.send_header("Content-type", "text/html")
        else:
            self.send_header("Content-type", type)
        self.end_headers()
        if errorCode == 404:
            self.wfile.write(
                bytes(jinja.get_template("error.html").render(name=conf.name, conf.version=conf.version, code=errorCode), "utf-8"))
        elif detect(open(filePath, "rb").read(1024)) == False:
            with open(filePath, "r") as file:
                self.wfile.write(bytes(file.read(), "utf-8"))
        else:
            with open(filePath, "rb") as file:
                self.wfile.write(file.read())


if __name__ == "__main__":
    webServer = HTTPServer((conf.hostname, conf.port), httpHandler)
    print("Server started http://%s:%s" % (conf.hostname, conf.port))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped.")
