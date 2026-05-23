import json
import tempfile
import unittest
from pathlib import Path

from omni_depth.cli import run_simulation


class SerialCliTest(unittest.TestCase):
    def test_simulation_writes_haptic_json_lines(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "messages.jsonl"

            run_simulation([3.2, 1.2, 0.3], output)

            payloads = [json.loads(line) for line in output.read_text().splitlines()]
            self.assertEqual([payload["level"] for payload in payloads], [0, 1, 2])
            self.assertEqual(payloads[0]["type"], "haptic")


if __name__ == "__main__":
    unittest.main()
