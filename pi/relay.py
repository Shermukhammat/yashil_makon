import RPi.GPIO as GPIO
import time
import sys

RELAY_PINS = [11, 13]
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

for pin in RELAY_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)  # Start OFF (assuming active LOW relay)


def control_relay(pin: int, state: bool):
    """
    Control a relay connected to the given GPIO pin.

    Args:
        pin (int): GPIO pin number.
        state (bool): True for ON, False for OFF.
    """
    if state:
        print(f"Relay on pin {pin} ON")
        GPIO.output(pin, GPIO.LOW)  # Active LOW relay
    else:
        print(f"Relay on pin {pin} OFF")
        GPIO.output(pin, GPIO.HIGH)


if __name__ == "__main__":
    # Example usage: python3 relay.py 17 1
    if len(sys.argv) < 3:
        print("Usage: python3 relay.py [PIN] [1=ON | 0=OFF]")
        sys.exit()

    pin = int(sys.argv[1])
    state = sys.argv[2] == '1'

    if pin not in RELAY_PINS:
        print(f"Invalid pin. Choose from {RELAY_PINS}")
        sys.exit()

    control_relay(pin, state)