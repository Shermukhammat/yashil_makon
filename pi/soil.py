import time
import board
import busio
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn

# ADC setup
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS1115(i2c)
chan = AnalogIn(ads, 0)

# Calibration values
RAW_DRY = 16718     # dry soil value
RAW_WET = 7861      # wet soil value

# Smooth ADC noise
def get_avg_reading(samples=10, delay=0.02) -> float:
    """
    Read multiple ADC samples and return the averaged value.
    This helps reduce noise and produce a stable reading.

    Args:
        samples (int, optional):
            Number of ADC readings to average.
            More samples = smoother result but slower. Defaults to 10.
        
        delay (float, optional):
            Delay (in seconds) between each sample to stabilize readings.
            Defaults to 0.02 seconds.

    Returns:
        float:
            The averaged raw ADC reading from the ADS1115.
    """
    
    values = []
    for _ in range(samples):
        values.append(chan.value)
        time.sleep(delay)
    return sum(values) / len(values)

def measure_moisture() -> tuple[int, float, int, float]:
    """
    Measure soil moisture using a capacitive sensor connected to an ADS1115 ADC.

    The function:
    - Reads averaged ADC data (reduces noise)
    - Converts raw ADC value to a moisture percentage using calibration values
    - Clamps the result to 0–100%
    - Computes a normalized value (0.0–1.0) ideal for ML models or logging
    - Returns moisture %, normalized moisture, raw ADC, and voltage

    Returns:
        tuple:
            moisture_percent (int):
                Moisture level in percent (0–100).
            
            normalized (float):
                Moisture normalized to 0.0–1.0 range. Good for ML models.
            
            raw (int):
                The averaged raw ADC value from the ADS1115.
            
            voltage (float):
                The measured voltage from the ADS1115 for monitoring/debugging.
    """

    raw = get_avg_reading(samples=10, delay=0.1)
    voltage = chan.voltage

    moisture = (RAW_DRY - raw) / (RAW_DRY - RAW_WET) * 100
    moisture = max(0, min(100, moisture)) # clamp

    # good for ML
    normalized = moisture / 100

    return round(moisture), round(normalized, 4), int(raw), voltage


if __name__ == '__main__':
    while True:
        moisture, norm, raw, voltage = measure_moisture()
        print(f"Moisture: {moisture}%  Normalized: {norm}  Raw: {raw}  Volt: {voltage:.4f}")
        time.sleep(1)
