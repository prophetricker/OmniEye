# Hardware Bring-up Checklist

## 1. Repository

Owner: Codex can run these checks.

```powershell
cd D:\MyProject\Bohack2\OmniEye
.\scripts\run_tests.ps1
git status --short
```

Expected: tests pass and `git status --short` prints nothing.

## 2. ESP32 OLED Output Loop

Owner: user handles physical wiring and flashing. Codex can inspect Windows serial ports once the ESP32 is plugged in.

1. On the physical board, wire the OLED from the screen-facing pin order `GND VCC SCL SDA`.
2. Connect `OLED GND -> ESP32 GND`.
3. Connect `OLED VCC -> ESP32 3V3`.
4. Connect `OLED SCL -> ESP32 GPIO9`.
5. Connect `OLED SDA -> ESP32 GPIO8`.
6. Plug the ESP32 into the Windows laptop with a USB data cable.
7. Ask Codex to run `.\scripts\list_serial_ports.ps1`, or run it yourself from `D:\MyProject\Bohack2\OmniEye`.
8. Expected result: one entry like `USB Serial Device (COMx)` is the ESP32. Use that `COMx` in the serial test.
9. Copy `esp32-firmware/micropython/main.py` and `esp32-firmware/micropython/ssd1306.py` to the ESP32 root.
10. Reset the ESP32.
11. Run:

```powershell
python -m omni_depth.cli serial-sim 3.2 1.2 0.6 0.3 --port COM7
```

Replace `COM7` with the detected ESP32 port.

Expected: the OLED updates `Level` and `Dist` as the simulated distance decreases.

## 3. X4 CameraSDK

Owner: user connects the X4. Codex can run SDK commands and inspect logs.

USB-first path:

1. Keep Windows WiFi connected to the internet so Codex remains usable.
2. Connect the Insta360 X4 to the Windows laptop with a USB-C data cable.
3. Keep the X4 powered on.
4. If the X4 asks for a USB mode, choose a mode that allows computer/USB access rather than charge-only.
5. Ask Codex to run the official `CameraSDKTest.exe`.
6. Expected result: the test program prints an X4 camera name, serial number, and firmware version, then opens the camera.

WiFi fallback path:

1. On the Insta360 X4, enable WiFi/hotspot mode from the camera quick settings.
2. On the Windows laptop, click the WiFi icon in the taskbar.
3. Select the X4 WiFi network. It is usually named like `X4 ******` or `Insta360 ******`.
4. Enter the X4 WiFi password shown on the camera screen or in the camera wireless settings.
5. Confirm Windows says it is connected to the X4 WiFi. Internet may be unavailable while connected; that is expected.
6. Ask Codex to run the official `CameraSDKTest.exe`.

After either path works, build and run `windows-agent`.

## 4. DAP

Owner: Codex can prepare commands. User may need to approve/install large GPU dependencies.

1. Use Python 3.10/3.11, not Python 3.14.
2. Install a CUDA-compatible PyTorch build for GTX1660Ti.
3. Keep DAP weights under `dap_weights/` or `models/`.
4. Export a `.npy` depth map and validate:

```powershell
python -m omni_depth.cli depth-map --input depth.npy --output message.jsonl
```
