import json
import sys
import time

from machine import Pin, PWM


MOTOR_PIN = 5
PWM_FREQ = 200
TIMEOUT_MS = 2000
LEVEL_TO_DUTY = {
    0: 0,
    1: 260,
    2: 520,
    3: 780,
    4: 1023,
}


motor = PWM(Pin(MOTOR_PIN, Pin.OUT), freq=PWM_FREQ, duty=0)
last_haptic_ms = time.ticks_ms()


def clamp_level(value):
    try:
        level = int(value)
    except (TypeError, ValueError):
        return 0
    return max(0, min(4, level))


def set_motor(level):
    motor.duty(LEVEL_TO_DUTY[clamp_level(level)])


def handle_line(line):
    global last_haptic_ms
    try:
        payload = json.loads(line)
    except ValueError:
        set_motor(0)
        return

    if payload.get("type") != "haptic":
        return

    set_motor(payload.get("level", 0))
    last_haptic_ms = time.ticks_ms()


def poll_stdin():
    line = sys.stdin.readline()
    if line:
        handle_line(line.strip())


while True:
    poll_stdin()
    if time.ticks_diff(time.ticks_ms(), last_haptic_ms) > TIMEOUT_MS:
        set_motor(0)
    time.sleep_ms(10)
