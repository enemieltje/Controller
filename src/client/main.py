import math
import time
import requests
from gpiozero import PWMLED, MCP3008
from time import sleep

# create an object called pot that refers to MCP3008 channel 0
x = MCP3008(0)
y = MCP3008(1)

while True:
    valuex = math.floor(x.value * 2**16)
    valuey = math.floor(y.value * 2**16)
    print(f"x: {valuex:05}, y: {valuey:05}", end="\r")
    sleep(0.01)

# for i in range(100):
#     requests.get('http://localhost:8080')
#     time.sleep(0.1)
