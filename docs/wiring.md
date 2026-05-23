# Wiring

## ESP32 to Vibration Motor Driver

Do not connect a vibration motor directly to an ESP32 GPIO. Use a MOSFET, transistor driver, or motor driver module.

Default firmware pin:

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
