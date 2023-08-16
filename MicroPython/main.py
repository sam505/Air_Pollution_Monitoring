from machine import Pin, ADC
import time
import network

# TODO: Store these credentials as environment variables
# ssid = "Galaxy A51 D22F"
# password = "tqmy4554"

ssid = "Home"
password = "Home123M1"

led = Pin(2, Pin.OUT)
mq7_analog = ADC(Pin(34, Pin.IN))

# connecting to Wi-Fi
lan = network.WLAN(network.STA_IF)
lan.active(True)

print("Network Status:", lan.scan())


def wifi_connect():
    if not lan.isconnected():
        print("Network Status:", lan.scan())
        lan.connect(ssid, password)
        while not lan.isconnected():
            time.sleep(5)
            pass
        print("Network Config:", lan.ifconfig())


def main():
    wifi_connect()
    while True:
        mq7_a = mq7_analog.read_u16()
        print("MQ7:", mq7_a)
        print("LED toggling...")
        led.on()
        time.sleep(0.1)
        led.off()
        time.sleep(0.1)
        led.on()
        time.sleep(0.1)
        led.off()
        time.sleep(0.7)


if __name__ == "__main__":
    main()
