# Known Limitations

- The current workstation does not have CMake/MSVC visible to this shell, so `windows-agent` has not been compiled here.
- DAP dependencies and weights are not installed in this environment.
- The MicroPython firmware assumes `sys.stdin.readline()` is usable over USB serial on the selected ESP32 firmware image.
- The current bring-up output is a 0.96 inch I2C SSD1306 OLED on SDA GPIO8 and SCL GPIO9. Motor PWM will be restored after display validation.
- Official `CameraSDKTest.exe` returned `no device found` while the X4 was connected by USB on this workstation. USB may require a different X4 USB mode, driver, cable, or the SDK may need the WiFi path for this device state.
- X4 WiFi may occupy the Windows network adapter, so cloud/API calls should be tested separately from the camera link.
- Monocular panoramic depth can fail on glass, reflective surfaces, low light, stairs, curbs, and moving obstacles.
