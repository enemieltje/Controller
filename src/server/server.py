from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from eventmap import event_map
# from uinputManager import device
import uinputManager
import uinput
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

hostName = "0.0.0.0"
serverPort = 8080

# x = 0
# for i in range(100):
#     x = x + 0.04
#     y = np.sin(x)
#     plt.scatter(x, y)
#     plt.title("Real Time plot")
#     plt.xlabel("x")
#     plt.ylabel("sinx")
#     plt.pause(0.05)

plt.show()


def plot(v):
    t = time.process_time()
    plt.scatter(t, v)
    plt.title("Sensor Values")
    plt.xlabel("t")
    plt.ylabel("v")
    plt.pause(0.05)


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
                    plot(value)
                    event_code = event_map.get(event)
                    # if event == "ABS_X":
                    #     uinputManager.rotate(
                    #         uinputManager.device, uinput.REL_X, value)
                    # if event == "ABS_Y":
                    #     uinputManager.rotate(
                    #         uinputManager.device, uinput.REL_Y, value)
                    # if event == "ABS_RX":
                    #     uinputManager.pan(
                    #         uinputManager.device, uinput.REL_X, value)
                    # if event == "ABS_RY":
                    #     uinputManager.pan(
                    #         uinputManager.device, uinput.REL_Y, value)

                    continue
                    if event_code:
                        # uinputManager.device.emit(event_code, value)
                        continue


def startServer():
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
