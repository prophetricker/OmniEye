import argparse
import sys
import time
from pathlib import Path

from .haptics import DistanceSmoother, classify_distance, make_haptic_message
from .roi import front_lower_roi, percentile_distance


def run_simulation(distances, output_path, confidence=0.9):
    smoother = DistanceSmoother(window_size=3)
    output = Path(output_path)
    with output.open("w", encoding="utf-8") as handle:
        for distance in distances:
            smoothed = smoother.add(distance)
            level = classify_distance(smoothed)
            handle.write(make_haptic_message(level, smoothed, confidence))


def send_simulation_to_serial(distances, port, baudrate=115200, interval_s=0.5):
    import serial

    smoother = DistanceSmoother(window_size=3)
    with serial.Serial(port, baudrate, timeout=1) as serial_port:
        for distance in distances:
            smoothed = smoother.add(distance)
            level = classify_distance(smoothed)
            serial_port.write(make_haptic_message(level, smoothed, 0.9).encode("utf-8"))
            time.sleep(interval_s)


def run_depth_map(depth_map_path, output_path):
    import numpy as np

    depth_map = np.load(depth_map_path)
    roi = front_lower_roi(depth_map)
    distance = percentile_distance(roi)
    level = classify_distance(distance)
    Path(output_path).write_text(make_haptic_message(level, distance or 0.0, 0.7), encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description="OmniEye depth-service utilities")
    subparsers = parser.add_subparsers(dest="command", required=True)

    simulate = subparsers.add_parser("simulate", help="Generate haptic JSON lines from distances")
    simulate.add_argument("distances", nargs="+", type=float)
    simulate.add_argument("--output", required=True)

    serial_sim = subparsers.add_parser("serial-sim", help="Send simulated haptic messages to ESP32")
    serial_sim.add_argument("distances", nargs="+", type=float)
    serial_sim.add_argument("--port", required=True)
    serial_sim.add_argument("--baudrate", type=int, default=115200)
    serial_sim.add_argument("--interval-s", type=float, default=0.5)

    depth_map = subparsers.add_parser("depth-map", help="Convert a .npy depth map into one haptic message")
    depth_map.add_argument("--input", required=True)
    depth_map.add_argument("--output", required=True)

    args = parser.parse_args(argv)
    if args.command == "simulate":
        run_simulation(args.distances, args.output)
    elif args.command == "serial-sim":
        send_simulation_to_serial(args.distances, args.port, args.baudrate, args.interval_s)
    elif args.command == "depth-map":
        run_depth_map(args.input, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
