import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
BUTTOM_SENSOR_PIN = 26            
GPIO.setup(BUTTOM_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def is_water_at_bottom() -> bool:
    return True if GPIO.input(BUTTOM_SENSOR_PIN) else False  # GPIO.input() returns 1 or 0
