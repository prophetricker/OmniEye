import tempfile
import unittest
from pathlib import Path

from omni_depth.frame_extraction import MissingDecoderError, extract_sampled_frames


class FakeCapture:
    def __init__(self, frame_count=10, fps=5.0):
        self.frame_count = frame_count
        self.fps = fps
        self.index = 0

    def isOpened(self):
        return True

    def get(self, prop):
        if prop == 5:
            return self.fps
        if prop == 7:
            return self.frame_count
        return 0

    def read(self):
        if self.index >= self.frame_count:
            return False, None
        frame = f"frame-{self.index}"
        self.index += 1
        return True, frame

    def release(self):
        pass


class FakeCv2:
    CAP_PROP_FPS = 5
    CAP_PROP_FRAME_COUNT = 7

    def __init__(self):
        self.writes = []

    def VideoCapture(self, path):
        self.input_path = path
        return FakeCapture()

    def imwrite(self, path, frame):
        self.writes.append((Path(path).name, frame))
        Path(path).write_text(str(frame), encoding="utf-8")
        return True


class FrameExtractionTest(unittest.TestCase):
    def test_extracts_frames_at_target_rate(self):
        fake_cv2 = FakeCv2()

        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "input.h264"
            output_dir = Path(tmpdir) / "frames"
            input_path.write_bytes(b"not-used-by-fake-capture")

            result = extract_sampled_frames(
                input_path,
                output_dir,
                sample_fps=1.0,
                max_frames=3,
                cv2_module=fake_cv2,
            )

            self.assertEqual(result.frames_written, 2)
            self.assertEqual(result.source_fps, 5.0)
            self.assertEqual([name for name, _ in fake_cv2.writes], ["frame_000001.jpg", "frame_000002.jpg"])
            self.assertEqual([frame for _, frame in fake_cv2.writes], ["frame-0", "frame-5"])

    def test_missing_decoder_has_actionable_error(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "input.h264"
            input_path.write_bytes(b"data")

            with self.assertRaises(MissingDecoderError) as context:
                extract_sampled_frames(input_path, Path(tmpdir) / "frames", cv2_module=None)

            self.assertIn("opencv-python", str(context.exception))


if __name__ == "__main__":
    unittest.main()
