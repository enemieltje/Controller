import math
import requests
from gpiozero import MCP3008

# create an object called pot that refers to MCP3008 channel 0
# x = MCP3008(0)
# y = MCP3008(1)

# while True:
#     valuex = math.floor(x.value * 2**16)
#     valuey = math.floor(y.value * 2**16)
#     print(f"x: {valuex:05}, y: {valuey:05}", end="\r")
#     requests.post('http://192.168.2.50:8080/uinput/emit',
#                   json={f"{uinput.ABS_X}": valuex, "ABS_Y": valuey})
#     sleep(0.01)

# for i in range(100):
#     requests.get('http://192.168.2.50:8080')
#     time.sleep(0.1)
channels = {}
rolling_averages = {}
data = {}
ri_max = 10
ri = 0


def set_axis(name, channel):
    channels[name] = MCP3008(channel)
    rolling_averages[name] = [0] * ri_max
    data[name] = 0


set_axis("ABS_X", 0)
set_axis("ABS_Y", 1)
set_axis("ABS_Z", 2)
set_axis("ABS_RX", 3)
set_axis("ABS_RY", 4)
set_axis("ABS_RZ", 5)

while True:
    for name, channel in channels.items():
        data[name] -= rolling_averages[name][ri]
        rolling_averages[name][ri] = math.floor(
            (channel.value * 2**16) / ri_max * 2)
        data[name] += rolling_averages[name][ri]
        ri = (ri + 1) % ri_max
    data["ABS_Z"] = int(data["ABS_Z"]*3/10)

    try:
        requests.post('http://192.168.2.50:8080/uinput/emit',
                      json=data)
    except ConnectionError:
        print("Server not responding", end="\r")
