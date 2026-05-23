# Hardware Bring-up Checklist

## 1. Repository

```powershell
cd D:\MyProject\Bohack2\OmniEye
.\scripts\run_tests.ps1
git status --short
```

## 2. ESP32 Haptic Loop

Owner: user handles physical wiring and plugging. Codex can inspect Windows serial ports once the ESP32 is plugged in.

1. On the physical helmet board, wire the motor through a driver module. Do not connect the motor directly to an ESP32 GPIO.
2. Plug the ESP32 into the Windows laptop with a USB data cable.
3. Ask Codex to run `.\scripts\list_serial_ports.ps1`, or run it yourself from `D:\MyProject\Bohack2\OmniEye`.
4. Expected result: one `USB 串行设备 (COMx)` or similar entry is `OK`. Use that `COMx` in the next command.
5. Copy `esp32-firmware/micropython/main.py` to the ESP32.
6. Run:

```powershell
python -m omni_depth.cli serial-sim 3.2 1.2 0.6 0.3 --port COM7
```

Replace `COM7` with the detected ESP32 port. Expected: vibration gets stronger as the simulated distance decreases.

## 3. X4 CameraSDK

Owner: user connects the Windows laptop to the X4 WiFi. Codex can then run SDK commands and inspect logs.

1. On the Insta360 X4, turn on the camera and enable its WiFi/hotspot mode from the camera quick settings.
2. On the Windows laptop, click the WiFi icon in the taskbar.
3. Select the X4 WiFi network. It is usually named like `X4 ******` or `Insta360 ******`.
4. Enter the X4 WiFi password shown on the camera screen or in the camera wireless settings.
5. Confirm Windows says it is connected to the X4 WiFi. Internet may be unavailable while connected; that is expected.
6. Ask Codex to run the official `CameraSDKTest.exe`, or run it manually from the SDK package.
7. Expected result: the test program prints an X4 camera name, serial number, and firmware version, then opens the camera.
8. Build and run `windows-agent`.

## 4. DAP

1. Use Python 3.10/3.11, not Python 3.14.
2. Install a CUDA-compatible PyTorch build for GTX1660Ti.
3. Keep DAP weights under `dap_weights/` or `models/`.
4. Export a `.npy` depth map and validate:

```powershell
python -m omni_depth.cli depth-map --input depth.npy --output message.jsonl
```
