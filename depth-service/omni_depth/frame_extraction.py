from dataclasses import dataclass
from pathlib import Path


class MissingDecoderError(RuntimeError):
    pass


@dataclass(frozen=True)
class FrameExtractionResult:
    frames_written: int
    source_fps: float
    output_dir: Path


def _load_cv2():
    try:
        import cv2  # type: ignore
    except ModuleNotFoundError as exc:
        raise MissingDecoderError(
            "OpenCV is required for frame extraction. Install it with: "
            "python -m pip install opencv-python"
        ) from exc
    return cv2


def extract_sampled_frames(
    input_path,
    output_dir,
    sample_fps=1.0,
    max_frames=0,
    cv2_module="auto",
):
    input_path = Path(input_path)
    output_dir = Path(output_dir)

    if sample_fps <= 0:
        raise ValueError("sample_fps must be greater than 0")
    if not input_path.exists():
        raise FileNotFoundError(input_path)

    if cv2_module == "auto":
        cv2_module = _load_cv2()
    elif cv2_module is None:
        raise MissingDecoderError(
            "OpenCV is required for frame extraction. Install it with: "
            "python -m pip install opencv-python"
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    capture = cv2_module.VideoCapture(str(input_path))
    if not capture.isOpened():
        raise RuntimeError(f"Could not open video stream: {input_path}")

    source_fps = float(capture.get(cv2_module.CAP_PROP_FPS) or 0.0)
    frame_interval = 1
    if source_fps > 0:
        frame_interval = max(1, round(source_fps / sample_fps))

    frames_written = 0
    frame_index = 0
    try:
        while True:
            ok, frame = capture.read()
            if not ok:
                break
            if frame_index % frame_interval == 0:
                output_path = output_dir / f"frame_{frames_written + 1:06d}.jpg"
                if not cv2_module.imwrite(str(output_path), frame):
                    raise RuntimeError(f"Failed to write frame: {output_path}")
                frames_written += 1
                if max_frames > 0 and frames_written >= max_frames:
                    break
            frame_index += 1
    finally:
        capture.release()

    return FrameExtractionResult(
        frames_written=frames_written,
        source_fps=source_fps,
        output_dir=output_dir,
    )
