
import math
import time
import uinput


events = (
    uinput.BTN_A,
    uinput.BTN_B,
    uinput.BTN_X,
    uinput.BTN_Y,
    uinput.BTN_TL,
    uinput.BTN_TR,
    uinput.BTN_LEFT,
    uinput.BTN_RIGHT,
    uinput.BTN_MIDDLE,
    uinput.BTN_THUMBL,
    uinput.BTN_THUMBR,
    uinput.KEY_UP,
    uinput.KEY_LEFT,
    uinput.KEY_RIGHT,
    uinput.KEY_DOWN,
    uinput.KEY_LEFTSHIFT,
    uinput.KEY_LEFTCTRL,
    uinput.REL_X,
    uinput.REL_Y,
    uinput.ABS_X + (0, 2**16, 0, 0),
    uinput.ABS_Y + (0, 2**16, 0, 0),
    uinput.ABS_Z + (0, 2**16, 0, 0),
    uinput.ABS_RX + (0, 2**16, 0, 0),
    uinput.ABS_RY + (0, 2**16, 0, 0),
    uinput.ABS_RZ + (0, 2**16, 0, 0),
)

device = uinput.Device(
    events,
    vendor=0x1d6b,
    product=0x0104,
    version=0x100,
    name="Custom Gamepad",
)


def test(device: uinput.Device):
    print("Test")

    device.emit(uinput.BTN_A, 1)
    # time.sleep(1)
    device.emit(uinput.BTN_A, 0)


def filter(value, center, dz_min, dz_max, scale):
    if dz_min < value < dz_max:
        return
    return math.floor((value - center)/scale)


def pan(device: uinput.Device, axis, value):
    value = filter(value, 33000, 30000, 36000, 3000)
    if not value:
        return

    device.emit(uinput.BTN_MIDDLE, 1)
    device.emit(axis, value)
    device.emit(uinput.BTN_MIDDLE, 0)


def rotate(device: uinput.Device, axis, value):
    print(f"value: {value}")
    value = filter(value, 33000, 30000, 36000, 10000)
    if not value:
        return
    print(f"filtered value: {value}")

    device.emit(uinput.KEY_LEFTSHIFT, 1)
    device.emit(uinput.BTN_MIDDLE, 1)
    device.emit(axis, value)
    device.emit(uinput.BTN_MIDDLE, 0)
    device.emit(uinput.KEY_LEFTSHIFT, 0)
