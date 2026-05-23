# Depth Service

The depth service converts distances or depth maps into OmniEye haptic JSON-line messages.

## Verified Unit Tests

```powershell
python -m unittest discover -s depth-service\tests -t depth-service
```

## Simulated Distance Output

```powershell
python -m omni_depth.cli simulate 3.2 1.2 0.6 0.3 --output messages.jsonl
```

## Send Simulated Haptic Messages to ESP32

```powershell
python -m omni_depth.cli serial-sim 3.2 1.2 0.6 0.3 --port COM7
```

## Depth Map Input

For DAP integration, save a metric depth map as `.npy`, then run:

```powershell
python -m omni_depth.cli depth-map --input depth.npy --output message.jsonl
```

The current MVP keeps DAP model weights outside Git under `dap_weights/` or `models/`.

## Extract Frames from X4 Preview Stream

The Windows agent writes raw preview stream bytes to `windows-agent/frames/preview_stream_0.h264`.
Install OpenCV, then sample low-rate JPEG frames for the depth pipeline:

```powershell
python -m pip install opencv-python
python -m omni_depth.cli extract-frames `
  --input ..\windows-agent\frames\preview_stream_0.h264 `
  --output-dir sampled-frames `
  --sample-fps 1 `
  --max-frames 5
```

This produces files such as `sampled-frames/frame_000001.jpg`. The MVP targets one frame every 1-2 seconds for DAP on a laptop GPU.

## Mock Frame-to-Haptic Link

Before DAP is wired in, use explicit mock distances to validate the frame-to-ESP32 protocol:

```powershell
python -m omni_depth.cli frames-mock-distance `
  --frames-dir sampled-frames `
  --distances 3.2 0.6 0.3 `
  --output mock-messages.jsonl
```

Send the same messages to the ESP32/OLED over USB serial:

```powershell
python -m omni_depth.cli frames-mock-distance `
  --frames-dir sampled-frames `
  --distances 3.2 0.6 0.3 `
  --port COM7 `
  --interval-s 0.4
```

This is a temporary protocol smoke test. The distances are supplied manually; DAP will replace this source while preserving the same `haptic` JSON-line output.
