from http.server import BaseHTTPRequestHandler, HTTPServer

# from uinputManager import device
import uinputManager
import uinput
import time

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)

        match self.path:
            case "/":
                print(__name__)
                # time.sleep(1)
                uinputManager.test(uinputManager.device)
            case "/uinput/emit":
                uinputManager.device.emit()

        self.send_response(200)
        # self.send_header("Content-type", "text/html")
        self.end_headers()
        # self.wfile.write(open("src/server/index.html").read().encode())


def startServer():
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
