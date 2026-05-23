# Known Limitations

- The current workstation does not have CMake/MSVC visible to this shell, so `windows-agent` has not been compiled here.
- DAP dependencies and weights are not installed in this environment.
- USB serial JSON lines did not update the OLED reliably through `sys.stdin.readline()` on this MicroPython image. The current reliable bring-up path is `mpremote exec "import main; main.show_haptic(level, distance)"`.
- The current bring-up output is a 0.96 inch I2C SSD1306 OLED on SDA GPIO8 and SCL GPIO9. Motor PWM will be restored after display validation.
- Official `CameraSDKTest.exe` returned `no device found` while the X4 was connected by USB on this workstation. Windows enumerated the X4 as USB storage, which is useful for file access but not sufficient for CameraSDK control in the current state.
- X4 WiFi may occupy the Windows network adapter, so cloud/API calls should be tested separately from the camera link.
- Monocular panoramic depth can fail on glass, reflective surfaces, low light, stairs, curbs, and moving obstacles.
