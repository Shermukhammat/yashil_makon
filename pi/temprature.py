import time
import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
PIN = 4  # GPIO4

def mesure_humidity_and_temp() -> tuple[int, int]:
    # returns humidty and temrature
    try:
        return Adafruit_DHT.read_retry(sensor, PIN)
    except:
        return None, None

