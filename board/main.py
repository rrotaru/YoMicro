# Yo app microcontroller.
# Lights up when sent a Yo, able to send Yo all when shaken.
import pyb
import math
import time

accel = pyb.Accel()
pyb.Switch().callback(lambda: print('∆', end=""))
leds = [pyb.LED(x) for x in range(1,5)]
usb = pyb.USB_VCP()

def dark():
    for led in leds: led.off()

def disco(duration):
    then = time.time()
    step = 1
    i = 0
    leds[0].toggle()
    while time.time() - then < duration:
        leds[i].toggle()
        if i == 3: step = -1
        if i == 0: step = 1
        i += step
        leds[i].toggle()
        pyb.delay(100)
    dark()

def is_shaking(x, y, z):
    return abs(math.sqrt(x*x+y*y+z*z) - 22.5) > 8

while True:
    data = usb.recv(1, timeout=100)
    if data.isdigit():
        disco(int(data))

    if is_shaking(accel.x(), accel.y(), accel.z()):
        usb.send('∆', timeout=100)
    pyb.delay(300)
