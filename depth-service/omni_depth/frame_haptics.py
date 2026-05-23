from dataclasses import dataclass
from pathlib import Path
import tempfile
import time

from .haptics import DistanceSmoother, classify_distance, make_haptic_message


@dataclass(frozen=True)
class FrameHapticResult:
    frames_processed: int
    output_path: Path


def list_frame_files(frames_dir):
    frames_dir = Path(frames_dir)
    return sorted(
        path for path in frames_dir.iterdir()
        if path.suffix.lower() in {".jpg", ".jpeg", ".png"}
    )


def frames_to_mock_haptics(frames_dir, distances, output_path, confidence=0.5):
    frame_files = list_frame_files(frames_dir)
    if not frame_files:
        raise ValueError(f"No frame files found in {frames_dir}")
    if not distances:
        raise ValueError("distances must contain at least one value")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    smoother = DistanceSmoother(window_size=3)

    with output_path.open("w", encoding="utf-8") as handle:
        for index, _frame_path in enumerate(frame_files):
            distance = float(distances[index % len(distances)])
            smoothed = smoother.add(distance)
            level = classify_distance(smoothed)
            handle.write(make_haptic_message(level, smoothed, confidence))

    return FrameHapticResult(
        frames_processed=len(frame_files),
        output_path=output_path,
    )


def send_mock_haptics_to_serial(
    frames_dir,
    distances,
    port,
    baudrate=115200,
    interval_s=0.5,
    serial_factory=None,
    sleep=time.sleep,
):
    if serial_factory is None:
        import serial

        serial_factory = serial.Serial

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "messages.jsonl"
        result = frames_to_mock_haptics(frames_dir, distances, output_path)

        with serial_factory(port, baudrate, timeout=1) as serial_port:
            for line in output_path.read_text(encoding="utf-8").splitlines():
                serial_port.write((line + "\n").encode("utf-8"))
                sleep(interval_s)

        return result
