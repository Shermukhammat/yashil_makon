import csv
from datetime import datetime, timedelta
import random

# Configuration
start_date = datetime(2025, 12, 1)
days = 30
blocks = ["morning", "noon", "evening", "night"]
samples_per_block = 6  # e.g., 6 samples per block (every ~1–2 hours)

# Initialize list to hold rows
rows = []

# Track cumulative watering for history columns
watering_history = []

for day in range(days):
    current_date = start_date + timedelta(days=day)
    
    # Calculate watering history sums
    last_1d = watering_history[-1] if len(watering_history) >= 1 else 0
    last_2d = sum(watering_history[-2:]) if len(watering_history) >= 2 else last_1d
    last_3d = sum(watering_history[-3:]) if len(watering_history) >= 3 else last_2d
    last_1w = sum(watering_history[-7:]) if len(watering_history) >= 7 else last_3d

    # Randomly choose one block to water
    water_block = random.choice(blocks)
    duration = random.randint(20, 60)  # watering duration in minutes
    start_time_min = random.randint(0, 120) if water_block != "night" else 0

    # Track daily watering total for history
    daily_watered = duration if water_block != "night" else 0
    watering_history.append(daily_watered)

    for block in blocks:
        # Simulate sensor readings for the block
        temp_samples = [random.randint(18, 25) for _ in range(samples_per_block)]
        hum_samples = [random.randint(30, 50) for _ in range(samples_per_block)]
        moist_samples = [random.randint(25, 40) for _ in range(samples_per_block)]

        air_temp_mean = sum(temp_samples) / samples_per_block
        air_temp_min = min(temp_samples)
        air_temp_max = max(temp_samples)

        air_hum_mean = sum(hum_samples) / samples_per_block
        air_hum_min = min(hum_samples)
        air_hum_max = max(hum_samples)

        soil_moist_mean = sum(moist_samples) / samples_per_block
        soil_moist_min = min(moist_samples)
        soil_moist_max = max(moist_samples)

        if block == water_block:
            st_min = start_time_min
            dur = duration
        else:
            st_min = 0
            dur = 0

        row = [
            current_date.strftime("%Y-%m-%d"),
            block,
            round(air_temp_mean, 1),
            air_temp_min,
            air_temp_max,
            round(air_hum_mean, 1),
            air_hum_min,
            air_hum_max,
            round(soil_moist_mean, 1),
            soil_moist_min,
            soil_moist_max,
            last_1d,
            last_2d,
            last_3d,
            last_1w,
            st_min,
            dur
        ]
        rows.append(row)

# Write CSV
with open("watering_30days_sample.csv", "w", newline="") as f:
    writer = csv.writer(f)
    # header
    writer.writerow([
        "date", "day_part",
        "air_temp_mean", "air_temp_min", "air_temp_max",
        "air_hum_mean", "air_hum_min", "air_hum_max",
        "soil_moist_mean", "soil_moist_min", "soil_moist_max",
        "watering_24h", "watering_2d", "watering_in_3d", "watering_in_1w",
        "start_time_min", "duration"
    ])
    writer.writerows(rows)

print("30-day sample CSV with min, max, mean generated: watering_30days_sample.csv")
