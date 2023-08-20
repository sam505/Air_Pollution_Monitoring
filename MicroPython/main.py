from machine import Pin, ADC
import time
import dht
import network

# TODO: Store these credentials as environment variables
ssid = "network"
password = "network@123"

# ssid = "Home"
# password = "Home123M1"

led = Pin(2, Pin.OUT)
mq7_analog = ADC(Pin(34))
mq8_analog = ADC(Pin(32))
mq135_analog = ADC(Pin(33))

mq7_digital = Pin(14, Pin.IN)
mq8_digital = Pin(27, Pin.IN)
mq135_digital = Pin(26, Pin.IN)


dht_pin = 25
dht_sensor = dht.DHT11(Pin(dht_pin))


def wifi_connect():
    """
    Function to connect to wifi
    :return:
    """
    lan = network.WLAN(network.STA_IF)
    lan.active(True)
    if not lan.isconnected():
        print("Network Status:", lan.scan())
        lan.connect(ssid, password)
        while not lan.isconnected():
            time.sleep(5)
            pass
        print("Network Config:", lan.ifconfig())


def get_temp_humidity():
    dht_sensor.measure()
    temp = dht_sensor.temperature()
    humidity = dht_sensor.humidity()

    return temp, humidity


def blink_led():
    """

    :return:
    """
    led.on()
    time.sleep(0.1)
    led.off()
    time.sleep(0.1)
    led.on()
    time.sleep(0.1)
    led.off()
    time.sleep(0.7)


def get_sensors_data():
    mq7_a = mq7_analog.read_u16()
    mq8_a = mq8_analog.read_u16()
    mq135_a = mq135_analog.read_u16()

    mq7_d = mq7_digital.value()
    mq8_d = mq8_digital.value()
    mq135_d = mq135_digital.value()

    return mq7_a, mq8_a, mq135_a, mq7_d, mq8_d, mq135_d


def main():
    """
    Main function to run the logic

    :return:
    """
    wifi_connect()
    while True:
        sensors_data = get_sensors_data()
        print("Sensors:", sensors_data)
        print("LED toggling...")
        print(get_temp_humidity())
        blink_led()


if __name__ == "__main__":
    main()
