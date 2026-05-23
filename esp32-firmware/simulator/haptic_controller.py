import json


LEVEL_TO_DUTY = {
    0: 0,
    1: 260,
    2: 520,
    3: 780,
    4: 1023,
}


class HapticController:
    def __init__(self, timeout_ms=2000):
        self.timeout_ms = timeout_ms
        self._duty = 0
        self._last_haptic_ms = None
        self._level = 0
        self._distance_m = None

    def apply_message(self, line, now_ms):
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            self._duty = 0
            self._last_haptic_ms = None
            self._level = 0
            self._distance_m = None
            return self._duty

        if payload.get("type") != "haptic":
            return self.current_duty(now_ms)

        level = int(payload.get("level", 0))
        level = max(0, min(4, level))
        self._duty = LEVEL_TO_DUTY[level]
        self._level = level
        self._distance_m = payload.get("distance_m")
        self._last_haptic_ms = now_ms
        return self._duty

    def current_duty(self, now_ms):
        if self._last_haptic_ms is None:
            return 0
        if now_ms - self._last_haptic_ms > self.timeout_ms:
            self._duty = 0
            self._last_haptic_ms = None
            self._level = 0
            self._distance_m = None
        return self._duty

    def display_lines(self, now_ms):
        self.current_duty(now_ms)
        distance = "--" if self._distance_m is None else f"{float(self._distance_m):.2f}m"
        status = "USB serial OK" if self._last_haptic_ms is not None else "Waiting data"
        return [
            "OmniEye",
            f"Level: {self._level}",
            f"Dist: {distance}",
            status,
        ]
