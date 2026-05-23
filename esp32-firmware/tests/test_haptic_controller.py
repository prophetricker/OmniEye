import unittest

from simulator.haptic_controller import HapticController


class HapticControllerTest(unittest.TestCase):
    def test_maps_level_to_pwm_duty(self):
        controller = HapticController(timeout_ms=2000)

        self.assertEqual(controller.apply_message('{"type":"haptic","level":0}', now_ms=0), 0)
        self.assertEqual(controller.apply_message('{"type":"haptic","level":1}', now_ms=100), 260)
        self.assertEqual(controller.apply_message('{"type":"haptic","level":2}', now_ms=200), 520)
        self.assertEqual(controller.apply_message('{"type":"haptic","level":3}', now_ms=300), 780)
        self.assertEqual(controller.apply_message('{"type":"haptic","level":4}', now_ms=400), 1023)

    def test_ignores_non_haptic_messages(self):
        controller = HapticController(timeout_ms=2000)

        self.assertEqual(controller.apply_message('{"type":"speech","text":"hello"}', now_ms=0), 0)

    def test_stops_after_timeout(self):
        controller = HapticController(timeout_ms=2000)
        controller.apply_message('{"type":"haptic","level":3}', now_ms=100)

        self.assertEqual(controller.current_duty(now_ms=1500), 780)
        self.assertEqual(controller.current_duty(now_ms=2201), 0)

    def test_malformed_json_fails_closed(self):
        controller = HapticController(timeout_ms=2000)
        controller.apply_message('{"type":"haptic","level":3}', now_ms=100)

        self.assertEqual(controller.apply_message("not-json", now_ms=200), 0)


if __name__ == "__main__":
    unittest.main()
