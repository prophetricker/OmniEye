# Known Limitations

- The current workstation does not have CMake/MSVC visible to this shell, so `windows-agent` has not been compiled here.
- DAP dependencies and weights are not installed in this environment.
- USB serial JSON lines did not update the OLED reliably through `sys.stdin.readline()` on this MicroPython image. The current reliable bring-up path is `mpremote exec "import main; main.show_haptic(level, distance)"`.
- The current bring-up output is a 0.96 inch I2C SSD1306 OLED on SDA GPIO8 and SCL GPIO9. Motor PWM will be restored after display validation.
- Official `CameraSDKTest.exe` returned `no device found` while the X4 was connected by USB on this workstation. `File transfer` exposes storage only; `USB camera` exposes UVC webcam output. CameraSDK bring-up should use `Android phone control` plus a libusbK-compatible Windows driver.
- If `Android phone control` still produces `no device found`, the likely causes are missing libusbK driver binding, a charge-only/unstable USB cable, or outdated X4 firmware. Confirm the current X4 firmware on the camera before changing architecture.
- Monocular panoramic depth can fail on glass, reflective surfaces, low light, stairs, curbs, and moving obstacles.
