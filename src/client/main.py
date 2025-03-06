import time
import requests
from gpiozero import PWMLED, MCP3008
from time import sleep

# create an object called pot that refers to MCP3008 channel 0
pot = MCP3008(0)

while True:
    print(pot.value)
    sleep(0.1)

# for i in range(100):
#     requests.get('http://localhost:8080')
#     time.sleep(0.1)
