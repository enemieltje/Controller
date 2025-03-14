import math
import time
import requests
from gpiozero import MCP3008, Button
import adafruit_bno055
import board

i2c = board.I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c)
sensor.mode = adafruit_bno055.IMUPLUS_MODE
buttons = [Button(5),
           Button(6),
           Button(13),
           Button(19),
           Button(26)]

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
global mx0, my0, mz0
(mx0, my0, mz0) = sensor.euler


def calibrate():
    global mx0, my0, mz0
    (mx0, my0, mz0) = sensor.euler


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
print("")
print("")
print("")
t_old = time.process_time()
(ax, ay, az) = (0, 0, 0)
(vx, vy, vz) = (0, 0, 0)
(x, y, z) = (0, 0, 0)
posx = 0
xadjust = 0
while True:
    t = time.process_time()
    dt = t - t_old
    t_old = t

    (ax, ay, az) = sensor.linear_acceleration
    (mx, my, mz) = sensor.euler
    # if ax:
    #     (vx, vy, vz) = (vx + (ax * dt), vy + (ay * dt), vz + (az * dt))
    #     (x, y, z) = (x + (0.5 * ax * dt * dt), y +
    #                  (0.5 * ay * dt * dt), z + (0.5 * az * dt * dt))

    # xadjust = 0.5*dt*dt*ax
    # if math.fabs(ax) > 1:
    #     posx += xadjust

    # print("\033[1A\x1b[2K"*4)
    # print(f"t: {t}, dt: {dt}")
    # print(f"a: {ax}, {ay}, {az}")
    # print(f"v: {vx:6.1}, {vy:6.1}, {vz:6.1}")
    # print(f"pos: {posx}, {xadjust}, {z}")
    # print(f"mag: {mx:4.2}, {my:4.2}, {mz:4.2}")
    # # time.sleep(1)
    # data["AX"] = ax
    # data["AY"] = ay
    # data["AZ"] = az
    # data["VX"] = vx
    # data["VY"] = vy
    # data["VZ"] = vz
    # data["X"] = posx
    # data["Y"] = y
    # data["Z"] = z
    data["MX"] = float(mx or 0) - mx0
    data["MY"] = float(my or 0) - my0
    data["MZ"] = float(mz or 0) - mz0

    for name, channel in channels.items():
        data[name] -= rolling_averages[name][ri]
        rolling_averages[name][ri] = math.floor(
            (channel.value * 2**16) / ri_max * 2)
        data[name] += rolling_averages[name][ri]
        ri = (ri + 1) % ri_max
    data["ABS_RZ"] = math.floor((data["ABS_Z"]-22400)*10/3)

    for i in range(len(buttons)):
        if buttons[i].is_pressed:
            data[f"BTN_{i}"] = 1
            if i == 0:
                print(f"calibrate: {mx}, {my}, {mz}")
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
