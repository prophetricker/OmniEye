import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from omni_depth import cli
from omni_depth.cli import run_simulation


class SerialCliTest(unittest.TestCase):
    def test_simulation_writes_haptic_json_lines(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "messages.jsonl"

            run_simulation([3.2, 1.2, 0.3], output)

            payloads = [json.loads(line) for line in output.read_text().splitlines()]
            self.assertEqual([payload["level"] for payload in payloads], [0, 1, 2])
            self.assertEqual(payloads[0]["type"], "haptic")

    def test_extract_frames_command_invokes_extractor(self):
        calls = []

        def fake_extract(input_path, output_dir, sample_fps, max_frames):
            calls.append((Path(input_path), Path(output_dir), sample_fps, max_frames))
            return cli.FrameExtractionResult(
                frames_written=2,
                source_fps=5.0,
                output_dir=Path(output_dir),
            )

        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "preview.h264"
            output_dir = Path(tmpdir) / "frames"
            input_path.write_bytes(b"data")

            with redirect_stdout(StringIO()):
                exit_code = cli.main(
                    [
                        "extract-frames",
                        "--input",
                        str(input_path),
                        "--output-dir",
                        str(output_dir),
                        "--sample-fps",
                        "1.5",
                        "--max-frames",
                        "4",
                    ],
                    extract_frames=fake_extract,
                )

        self.assertEqual(exit_code, 0)
        self.assertEqual(calls, [(input_path, output_dir, 1.5, 4)])


if __name__ == "__main__":
    unittest.main()
