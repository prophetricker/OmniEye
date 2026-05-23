# Windows Agent

`omnieye_windows_agent` connects to the Insta360 X4 through the official Windows CameraSDK, starts the preview stream, and writes stream bytes to `frames/preview_stream_0.h264`.

## Build

Install Visual Studio Build Tools with MSVC and CMake, then run from `OmniEye/windows-agent`:

```powershell
cmake -S . -B build -G "Visual Studio 17 2022" -A x64 `
  -DCAMERA_SDK_ROOT="D:/MyProject/Bohack2/.sdk_extract/windows/Windows_CameraSDK-2.1.1_MediaSDK-3.1.3/CameraSDK/CameraSDK-20250812_192505-2.1.1-win64"
cmake --build build --config Release
```

## Run

Connect Windows to the X4 WiFi network first.

```powershell
.\build\Release\omnieye_windows_agent.exe --output-dir frames --seconds 30
```

If it cannot discover the camera, run the official `CameraSDKTest.exe` from the SDK package to validate the X4 WiFi connection before debugging OmniEye.
