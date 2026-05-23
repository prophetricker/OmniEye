# OmniEye Architecture

## MVP

```mermaid
flowchart LR
    X4[Insta360 X4] -->|USB Android phone control| Win[Windows laptop]
    Win -->|CameraSDK preview stream| Agent[windows-agent]
    Agent -->|frames| Depth[depth-service]
    Depth -->|JSON line haptic command| Serial[USB serial]
    Serial --> ESP32[ESP32 firmware]
    ESP32 -->|PWM| Motor[Vibration motor driver]
```

## Runtime Responsibilities

- Windows owns X4 CameraSDK integration, frame extraction, and depth estimation.
- The X4 USB mode for CameraSDK bring-up is `Android phone control`, not `File transfer` or `USB camera`.
- ESP32 owns motor safety behavior and stops vibration if haptic messages time out.
- Future speech messages reuse the same JSON-line serial channel.

## Serial Messages

Haptic:

```json
{"type":"haptic","level":3,"distance_m":0.72,"confidence":0.81}
```

Speech placeholder:

```json
{"type":"speech","text":"前方一米有障碍物"}
```
