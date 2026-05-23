import argparse
import sys
import time
from pathlib import Path

from .haptics import DistanceSmoother, classify_distance, make_haptic_message


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

    args = parser.parse_args(argv)
    if args.command == "simulate":
        run_simulation(args.distances, args.output)
    elif args.command == "serial-sim":
        send_simulation_to_serial(args.distances, args.port, args.baudrate, args.interval_s)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
