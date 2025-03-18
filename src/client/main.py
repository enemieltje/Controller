import math
import time
import requests
from gpiozero import MCP3008, Button
import adafruit_bno055
import board

i2c = board.I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c)
sensor.mode = adafruit_bno055.IMUPLUS_MODE
buttons = [
    Button(26, pull_up=True),
    Button(19, pull_up=True),
    Button(13, pull_up=True),
    Button(6, pull_up=True),
    Button(5, pull_up=True),
    Button(21, pull_up=True),
    Button(20, pull_up=True),
    Button(16, pull_up=True),
    Button(24, pull_up=True),
    Button(23, pull_up=True),
    Button(12, pull_up=True),
    Button(25, pull_up=True),
]

channels = {}
rolling_averages = {}
data = {}
ri_max = 10
ri = 0
global x0, y0, z0
(x0, y0, z0) = sensor.euler


def calibrate():
    global x0, y0, z0
    print(f"calibrate old: {x0}, {y0}, {z0}")
    (x0, y0, z0) = sensor.euler
    print(f"calibrate new: {x0}, {y0}, {z0}")


def set_axis(name, channel):
    channels[name] = MCP3008(channel)
    rolling_averages[name] = [0] * ri_max
    data[name] = 0


# set_axis("ABS_X", 0)
# set_axis("ABS_Y", 1)
# set_axis("ABS_Z", 2)
# set_axis("ABS_RX", 3)
# set_axis("ABS_RY", 4)
# set_axis("ABS_RZ", 5)
time.sleep(1)
calibrate()

while True:

    (x, y, z) = sensor.euler
    (qw, qx, qy, qz) = sensor.quaternion

    data["MX"] = float(x or 0) - x0
    data["MY"] = float(y or 0) - y0
    data["MZ"] = float(z or 0) - z0

    data["QW"] = float(qw or 0)
    data["QX"] = float(qx or 0)
    data["QY"] = float(qy or 0)
    data["QZ"] = float(qz or 0)

    # for name, channel in channels.items():
    #     data[name] -= rolling_averages[name][ri]
    #     rolling_averages[name][ri] = math.floor(
    #         (channel.value * 2**16) / ri_max * 2)
    #     data[name] += rolling_averages[name][ri]
    #     ri = (ri + 1) % ri_max
    # data["ABS_RZ"] = math.floor((data["ABS_Z"]-22400)*10/3)

    for i in range(len(buttons)):
        if buttons[i].is_pressed:
            data[f"BTN_{i}"] = 1
            if i == 9:
                calibrate()
        else:
            data[f"BTN_{i}"] = 0

    try:
        requests.post('http://192.168.2.50:8080/uinput/emit',
                      json=data)
    except ConnectionRefusedError:
        print("Server not responding", end="\r")
    except ConnectionError:
        print("Server not responding", end="\r")
