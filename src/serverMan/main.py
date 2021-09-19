import os.path
from http.server import BaseHTTPRequestHandler, HTTPServer
import mimetypes
import config
# import fire
print("ServerMan " + config.version)


hostName = "localhost"
serverPort = 8080


class httpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        errorCode = 200
        if self.path == "/":
            filePath = "./public/index.html"
        else:
            filePath = "./public" + self.path
            if not os.path.isfile(filePath):
                filePath = "./templates/404.html"
                errorCode = 404
        detect = lambda bytes: bool(bytes.translate(None, bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})))
        self.send_response(errorCode)
        type = mimetypes.guess_type(self.path)
        if type == None:
            self.send_header("Content-type", "text/html")
        else:
            self.send_header("Content-type", type)
        self.end_headers()
        if detect(open(filePath, "rb").read(1024)) == False:
            with open(filePath, "r") as file:
                self.wfile.write(bytes(file.read(), "utf-8"))
        else:
            with open(filePath, "rb") as file:
                self.wfile.write(file.read())


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), httpHandler)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
