import machine
import time

led = machine.Pin(2, machine.Pin.OUT)

while True:
    print("LED toggling...")
    led.on()
    time.sleep(0.1)
    led.off()
    time.sleep(0.1)
    led.on()
    time.sleep(0.1)
    led.off()
    time.sleep(0.7)
