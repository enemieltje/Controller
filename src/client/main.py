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


def set_axis(name, channel):
    channels[name] = MCP3008(channel)


set_axis("ABS_X", 0)
set_axis("ABS_Y", 1)
set_axis("ABS_Z", 2)
set_axis("RABS_X", 3)
set_axis("RABS_Y", 4)
set_axis("RABS_Z", 5)

while True:
    data = {}
    for name, channel in channels.items():
        data[name] = math.floor(channel.value * 2**16)
    requests.post('http://192.168.2.50:8080/uinput/emit',
                  json=data)
