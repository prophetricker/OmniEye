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
