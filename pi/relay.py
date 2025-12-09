import RPi.GPIO as GPIO
import time
import sys

# 1. BCM to BOARD Pin Mapping for the relays
# Key is the BOARD pin (used by the caller), Value is the BCM pin (used by GPIO)
BOARD_TO_BCM = {
    11: 17,  # Physical Pin 11 -> BCM GPIO 17
    13: 27   # Physical Pin 13 -> BCM GPIO 27
}

# The pins used for setup must be the BCM values
RELAY_PINS = list(BOARD_TO_BCM.values()) 

GPIO.setwarnings(False)

# 2. IMPORTANT: Set mode to BCM to prevent conflict with soil.py
GPIO.setmode(GPIO.BCM)

for pin_bcm in RELAY_PINS:
    GPIO.setup(pin_bcm, GPIO.OUT)
    GPIO.output(pin_bcm, GPIO.HIGH)  # Start OFF (assuming active LOW relay)


def control_relay(pin_board: int, state: bool):
    """
    Control a relay using the convenient BOARD pin number,
    but executes the command using the required BCM pin.

    Args:
        pin_board (int): The physical BOARD pin number (11 or 13).
        state (bool): True for ON, False for OFF.
    """
    if pin_board not in BOARD_TO_BCM:
        print(f"Error: Pin {pin_board} is not a valid mapped relay pin.")
        return

    # Translate the BOARD pin to the BCM pin
    pin_bcm = BOARD_TO_BCM[pin_board]

    if state:
        print(f"Relay on BOARD pin {pin_board} (BCM {pin_bcm}) ON")
        GPIO.output(pin_bcm, GPIO.LOW)  # Active LOW relay
    else:
        print(f"Relay on BOARD pin {pin_board} (BCM {pin_bcm}) OFF")
        GPIO.output(pin_bcm, GPIO.HIGH)


if __name__ == "__main__":
    # Example usage: python3 relay.py 11 1
    if len(sys.argv) < 3:
        print("Usage: python3 relay.py [BOARD_PIN] [1=ON | 0=OFF]")
        sys.exit()

    pin = int(sys.argv[1])
    state = sys.argv[2] == '1'

    if pin not in BOARD_TO_BCM:
        print(f"Invalid pin. Choose from {list(BOARD_TO_BCM.keys())}")
        sys.exit()

    control_relay(pin, state)

else:
    control_relay(11, 0)
    control_relay(13, 0)