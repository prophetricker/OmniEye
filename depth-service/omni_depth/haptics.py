import json
import math
from collections import deque
from statistics import median


def classify_distance(distance_m):
    if distance_m is None:
        return 0
    try:
        distance = float(distance_m)
    except (TypeError, ValueError):
        return 0
    if math.isnan(distance) or distance <= 0:
        return 0
    if distance < 0.4:
        return 4
    if distance < 0.8:
        return 3
    if distance < 1.5:
        return 2
    if distance < 3.0:
        return 1
    return 0


class DistanceSmoother:
    def __init__(self, window_size=3):
        if window_size <= 0:
            raise ValueError("window_size must be positive")
        self._values = deque(maxlen=window_size)

    def add(self, distance_m):
        self._values.append(float(distance_m))
        return float(median(self._values))


def make_haptic_message(level, distance_m, confidence):
    payload = {
        "type": "haptic",
        "level": int(level),
        "distance_m": round(float(distance_m), 2),
        "confidence": round(float(confidence), 2),
    }
    return json.dumps(payload, separators=(",", ":")) + "\n"
