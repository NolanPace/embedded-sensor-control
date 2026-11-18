# Embedded Sensor & Control Platform

A hardware-optional ESP32 telemetry and control demonstrator. Firmware samples an analog input, filters voltage, calculates a bounded proportional-control value, drives an indicator output, and streams CSV telemetry over USB serial. A Python simulator allows exploration without a board.

## Run without hardware
```bash
python telemetry.py --simulate --count 100 --output telemetry.csv
python telemetry.py --input telemetry.csv
python -m unittest discover -s tests -v
```

## Firmware setup
Install PlatformIO and use `pio run` to build for `esp32dev`. Flash with `pio run -t upload`, then observe serial at 115200 baud. GPIO34 is analog input (3.3V maximum), GPIO25 is a digital indicator output. Do not connect mains, motors, inductive loads or unsafe voltages directly to the board. Calibrate ADC readings for your hardware.

## Included
- ESP32 Arduino firmware at `src/main.cpp`, PlatformIO configuration
- JSON-independent CSV telemetry generator/parser/statistics and validation
- Deterministic simulated sensor noise and filtering
- Unit tests and GitHub Actions

Hardware build and electrical performance must be validated with actual equipment before real use. MIT licensed.
