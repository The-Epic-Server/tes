from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os

f = open("settings.txt")
settings = f.read().split("\n")
f.close()

for setting in settings:

    if setting.startswith("port"):
        serverPort = int(setting.replace("port: ", ""))
    if setting.startswith("hostname"):
        hostName = setting.replace("hostname: ", "")
    if setting.startswith("main"):
        mainFile = setting.replace("main: ", "")

pages = os.listdir("pages") 
print(pages)
requestnum = 0

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        global requestnum
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        requestnum += 1
        print(requestnum)
        if requestnum == 1:
            for page in pages:
                if self.path.replace("/", "") + ".html" == page:
                    print("opening " + self.path)
                    with open("pages\\" + page) as f:
                        doc = f.read()
                        self.wfile.write(bytes(doc, "utf-8"))
            if self.path.replace("/", "") == "":
                print("opening home")
                with open("pages\\" + mainFile) as f:
                    doc = f.read()
                    self.wfile.write(bytes(doc, "utf-8"))
            if not self.path.replace("/", "") + ".html" in pages:
                print("opening 404")
                with open("pages\\404.html") as f:
                    doc = f.read()
                    self.wfile.write(bytes(doc, "utf-8"))
        elif requestnum > 1:
            requestnum = 0

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
