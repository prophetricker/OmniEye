# Distance Calibration

## Default Levels

| Distance | Level | Meaning |
| --- | ---: | --- |
| `> 3.0m` | 0 | no vibration |
| `1.5m - 3.0m` | 1 | weak |
| `0.8m - 1.5m` | 2 | medium |
| `0.4m - 0.8m` | 3 | strong |
| `< 0.4m` | 4 | urgent |

## Depth Aggregation

Use the front lower field of view as the first ROI. For each depth map, use a low percentile rather than the absolute minimum to reduce single-pixel noise. Smooth distances over three frames before classifying.

## Safety Note

Depth from a monocular panoramic model can fail on glass, reflections, darkness, stairs, curbs, and moving obstacles. Treat the haptic output as an assistive cue, not a safety guarantee.
