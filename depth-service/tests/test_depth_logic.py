import json
import math
import unittest

from omni_depth.haptics import DistanceSmoother, classify_distance, make_haptic_message


class DistanceLogicTest(unittest.TestCase):
    def test_classifies_distance_thresholds(self):
        cases = [
            (3.2, 0),
            (2.0, 1),
            (1.0, 2),
            (0.6, 3),
            (0.3, 4),
        ]

        for distance, expected_level in cases:
            with self.subTest(distance=distance):
                self.assertEqual(classify_distance(distance), expected_level)

    def test_invalid_distance_is_no_alert(self):
        self.assertEqual(classify_distance(None), 0)
        self.assertEqual(classify_distance(math.nan), 0)
        self.assertEqual(classify_distance(-1.0), 0)

    def test_smoother_returns_median_of_recent_values(self):
        smoother = DistanceSmoother(window_size=3)

        self.assertEqual(smoother.add(3.0), 3.0)
        self.assertEqual(smoother.add(0.4), 1.7)
        self.assertEqual(smoother.add(0.5), 0.5)
        self.assertEqual(smoother.add(2.0), 0.5)

    def test_haptic_message_is_json_line(self):
        line = make_haptic_message(level=3, distance_m=0.72, confidence=0.81)

        self.assertTrue(line.endswith("\n"))
        payload = json.loads(line)
        self.assertEqual(payload["type"], "haptic")
        self.assertEqual(payload["level"], 3)
        self.assertEqual(payload["distance_m"], 0.72)
        self.assertEqual(payload["confidence"], 0.81)


if __name__ == "__main__":
    unittest.main()
