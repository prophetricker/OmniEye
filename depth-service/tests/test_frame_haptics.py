import json
import tempfile
import unittest
from pathlib import Path

from omni_depth.frame_haptics import frames_to_mock_haptics, send_mock_haptics_to_serial


class FrameHapticsTest(unittest.TestCase):
    def test_frames_generate_haptic_json_lines(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            frames_dir = Path(tmpdir) / "frames"
            frames_dir.mkdir()
            (frames_dir / "frame_000002.jpg").write_bytes(b"two")
            (frames_dir / "frame_000001.jpg").write_bytes(b"one")
            output_path = Path(tmpdir) / "messages.jsonl"

            result = frames_to_mock_haptics(
                frames_dir=frames_dir,
                distances=[3.2, 0.6],
                output_path=output_path,
            )

            payloads = [json.loads(line) for line in output_path.read_text().splitlines()]
            self.assertEqual(result.frames_processed, 2)
            self.assertEqual([payload["type"] for payload in payloads], ["haptic", "haptic"])
            self.assertEqual([payload["level"] for payload in payloads], [0, 1])
            self.assertEqual([payload["distance_m"] for payload in payloads], [3.2, 1.9])

    def test_rejects_empty_frame_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaises(ValueError) as context:
                frames_to_mock_haptics(
                    frames_dir=Path(tmpdir),
                    distances=[1.0],
                    output_path=Path(tmpdir) / "messages.jsonl",
                )

            self.assertIn("No frame files", str(context.exception))

    def test_sends_generated_haptics_to_serial(self):
        writes = []

        class FakeSerialPort:
            def write(self, data):
                writes.append(data.decode("utf-8"))

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, traceback):
                return False

        def fake_serial_factory(port, baudrate, timeout):
            self.assertEqual(port, "COM7")
            self.assertEqual(baudrate, 115200)
            self.assertEqual(timeout, 1)
            return FakeSerialPort()

        with tempfile.TemporaryDirectory() as tmpdir:
            frames_dir = Path(tmpdir) / "frames"
            frames_dir.mkdir()
            (frames_dir / "frame_000001.jpg").write_bytes(b"one")

            result = send_mock_haptics_to_serial(
                frames_dir=frames_dir,
                distances=[0.6],
                port="COM7",
                serial_factory=fake_serial_factory,
                sleep=lambda _seconds: None,
            )

        self.assertEqual(result.frames_processed, 1)
        payload = json.loads(writes[0])
        self.assertEqual(payload["level"], 3)
        self.assertEqual(payload["distance_m"], 0.6)


if __name__ == "__main__":
    unittest.main()
