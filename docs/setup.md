# Setup Notes

## Required Tools

- Git
- Python 3.10 or 3.11 for DAP runtime. The current workstation has Python 3.14, which is enough for unit tests but not recommended for PyTorch/DAP.
- Visual Studio Build Tools with MSVC for `windows-agent`.
- ffmpeg or OpenCV for preview stream frame decoding.
- PyTorch CUDA build compatible with the laptop GPU.

## First Hardware Checks

1. User: connect the X4 to the Windows laptop with a USB-C data cable.
2. User: on the X4 USB prompt, choose `Android phone control`. Do not choose `File transfer` or `USB camera` for CameraSDK control.
3. Codex or user: run the official `CameraSDKTest.exe` from the provided SDK package.
4. Expected result: X4 serial number and firmware version are printed, and the camera opens.
5. User: plug ESP32 into the Windows laptop with a USB data cable.
6. Codex or user: run `.\scripts\list_serial_ports.ps1` to identify the ESP32 COM port.
7. Run the host-side haptic simulator tests before flashing firmware.

## Dependency Strategy

Heavy dependencies and model weights are intentionally not committed. Keep DAP weights under `dap_weights/` or `models/`, both ignored by Git.

## Depth Service Smoke Test

```powershell
cd D:\MyProject\Bohack2\OmniEye
python -m unittest discover -s depth-service\tests -t depth-service
python -m omni_depth.cli simulate 3.2 1.2 0.6 0.3 --output messages.jsonl
```
