
import time
import uinput


events = (
    uinput.BTN_A,
    uinput.BTN_B,
    uinput.BTN_X,
    uinput.BTN_Y,
    uinput.BTN_TL,
    uinput.BTN_TR,
    uinput.BTN_THUMBL,
    uinput.BTN_THUMBR,
    uinput.ABS_X + (0, 255, 0, 0),
    uinput.ABS_Y + (0, 255, 0, 0),
    uinput.ABS_Z + (0, 255, 0, 0),
    uinput.ABS_RX + (0, 255, 0, 0),
    uinput.ABS_RY + (0, 255, 0, 0),
    uinput.ABS_RZ + (0, 255, 0, 0),
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


def emit(device: uinput.Device, event, value):
    # device.emit()
    pass

# Center joystick
# syn=False to emit an "atomic" (128, 128) event.
# device.emit(uinput.ABS_X, 50, syn=False)
# device.emit(uinput.ABS_Y, 50)


# device.emit(uinput.BTN_A, 1)
# time.sleep(1)
# device.emit(uinput.BTN_A, 0)
