# Wiring

## ESP32 to 0.96 inch OLED Placeholder

Use this wiring for the current bring-up step. The OLED replaces the motor output and displays the received haptic level.

Your OLED pin order from the screen-facing side is:

```text
GND VCC SCL SDA
```

Wire it as:

| OLED pin | ESP32 pin | Notes |
| --- | --- | --- |
| GND | GND | Ground |
| VCC | 3V3 | Use 3.3V first. |
| SCL | GPIO 9 | I2C clock. |
| SDA | GPIO 8 | I2C data. |

Copy both files to the ESP32 root:

- `esp32-firmware/micropython/main.py`
- `esp32-firmware/micropython/ssd1306.py`

Expected display after serial data arrives:

```text
OmniEye
Level: 3
Dist: 0.72m
USB serial OK
```

## ESP32 to Vibration Motor Driver

Do not connect a vibration motor directly to an ESP32 GPIO. Use a MOSFET, transistor driver, or motor driver module.

This is the later motor stage after OLED validation. The current firmware targets the OLED.

| Signal | ESP32 | Notes |
| --- | --- | --- |
| Motor PWM | GPIO 5 | Change `MOTOR_PIN` in `esp32-firmware/micropython/main.py` if needed. |
| GND | GND | Common ground between ESP32 and motor driver. |
| Motor power | External 3.3V/5V as required | Match the motor and driver module rating. |

## Windows to ESP32

Use USB serial at `115200` baud. The Windows depth service sends JSON-line haptic messages to the COM port.

## Smoke Test

After flashing/copying `main.py` to the ESP32, run:

```powershell
python -m omni_depth.cli serial-sim 3.2 1.2 0.6 0.3 --port COM7
```

Replace `COM7` with the port shown in Device Manager.
