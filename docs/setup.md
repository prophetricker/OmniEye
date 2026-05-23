# Setup Notes

## Required Tools

- Git
- Python 3.10 or 3.11 for DAP runtime. The current workstation has Python 3.14, which is enough for unit tests but not recommended for PyTorch/DAP.
- Visual Studio Build Tools with MSVC for `windows-agent`.
- ffmpeg or OpenCV for preview stream frame decoding.
- PyTorch CUDA build compatible with the laptop GPU.

## First Hardware Checks

1. Connect the Windows laptop to the X4 WiFi network.
2. Run the official `CameraSDKTest.exe` from the provided SDK package.
3. Confirm the X4 is discovered and can be opened.
4. Connect ESP32 over USB and identify its COM port in Device Manager.
5. Run the host-side haptic simulator tests before flashing firmware.

## Dependency Strategy

Heavy dependencies and model weights are intentionally not committed. Keep DAP weights under `dap_weights/` or `models/`, both ignored by Git.
