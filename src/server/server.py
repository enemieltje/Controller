from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from eventmap import event_map
# from uinputManager import device
import uinputManager
import uinput
import time

hostName = "0.0.0.0"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):

    def log_request(self, *args) -> None:
        pass
        # return super().log_message(format, *args)

    def do_GET(self):
        # print(self.path)

        match self.path:
            case "/":
                print(__name__)
                # time.sleep(1)
                uinputManager.test(uinputManager.device)

        self.send_response(200)
        # self.send_header("Content-type", "text/html")
        self.end_headers()
        # self.wfile.write(open("src/server/index.html").read().encode())

    def do_POST(self):

        self.send_response(200)
        self.end_headers()

        match self.path:
            case "/":
                print(__name__)
                # time.sleep(1)
                uinputManager.test(uinputManager.device)
            case "/uinput/emit":
                pass
                jsonString = self.rfile.read(
                    int(self.headers['Content-Length']))
                data = json.loads(jsonString)

                for event, value in data.items():
                    print(f" e: {event}, v: {value}")
                    event_code = event_map.get(event)
                    if not event_code:
                        continue
                    uinputManager.device.emit(event_code, value)


def startServer():
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
