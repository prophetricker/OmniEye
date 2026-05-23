# Hardware Bring-up Checklist

## 1. Repository

```powershell
cd D:\MyProject\Bohack2\OmniEye
.\scripts\run_tests.ps1
git status --short
```

## 2. ESP32 Haptic Loop

1. Wire the motor through a driver module.
2. Copy `esp32-firmware/micropython/main.py` to the ESP32.
3. Find the ESP32 COM port in Device Manager.
4. Run:

```powershell
python -m omni_depth.cli serial-sim 3.2 1.2 0.6 0.3 --port COM7
```

Expected: vibration gets stronger as the simulated distance decreases.

## 3. X4 CameraSDK

1. Connect Windows to the X4 WiFi network.
2. Run the official `CameraSDKTest.exe`.
3. Confirm the X4 is discovered and opens.
4. Build and run `windows-agent`.

## 4. DAP

1. Use Python 3.10/3.11, not Python 3.14.
2. Install a CUDA-compatible PyTorch build for GTX1660Ti.
3. Keep DAP weights under `dap_weights/` or `models/`.
4. Export a `.npy` depth map and validate:

```powershell
python -m omni_depth.cli depth-map --input depth.npy --output message.jsonl
```
