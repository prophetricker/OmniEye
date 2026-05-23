# OmniEye

OmniEye is a hackathon MVP for a blind-assistive perception helmet built around an Insta360 X4, a Windows laptop, and an ESP32 haptic controller.

## MVP Data Flow

```text
Insta360 X4 --X4 WiFi--> Windows laptop --USB serial--> ESP32 --PWM/GPIO--> vibration motor driver
```

The first milestone focuses on distance-to-obstacle haptic feedback. Semantic scene description and speech output are reserved for a later milestone.

## Project Layout

- `windows-agent/` - C++ CameraSDK agent for X4 discovery, preview streaming, and frame extraction.
- `depth-service/` - Python distance classification and DAP integration.
- `esp32-firmware/` - ESP32 firmware and host-side behavior simulator.
- `docs/` - wiring, setup, calibration, and troubleshooting notes.

## Current Verified Commands

```powershell
python -m unittest discover -s depth-service\tests -t depth-service
python -m unittest discover -s esp32-firmware\tests -t esp32-firmware
```

## Hardware Defaults

- X4 connects to Windows through X4 WiFi.
- ESP32 connects to Windows through USB serial.
- Vibration motor must be driven by a transistor/MOSFET/driver module, not directly from an ESP32 GPIO.
