# Known Limitations

- The current workstation does not have CMake/MSVC visible to this shell, so `windows-agent` has not been compiled here.
- DAP dependencies and weights are not installed in this environment.
- The MicroPython firmware assumes `sys.stdin.readline()` is usable over USB serial on the selected ESP32 firmware image.
- X4 WiFi may occupy the Windows network adapter, so cloud/API calls should be tested separately from the camera link.
- Monocular panoramic depth can fail on glass, reflective surfaces, low light, stairs, curbs, and moving obstacles.
