import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
SENSOR_PIN = 26            
GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def is_water_at_bottom() -> bool:
    return True if GPIO.input(SENSOR_PIN) else False  # GPIO.input() returns 1 or 0
