import json
import sys
import time

from machine import I2C, Pin
import ssd1306

try:
    import select
except ImportError:
    import uselect as select


I2C_SDA_PIN = 8
I2C_SCL_PIN = 9
OLED_WIDTH = 128
OLED_HEIGHT = 64
TIMEOUT_MS = 2000


i2c = I2C(0, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN))
display = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)
last_haptic_ms = None
current_level = 0
current_distance = None
last_drawn_state = None

poller = select.poll()
poller.register(sys.stdin, select.POLLIN)


def clamp_level(value):
    try:
        level = int(value)
    except (TypeError, ValueError):
        return 0
    return max(0, min(4, level))


def draw_status(status):
    global last_drawn_state
    state = (current_level, current_distance, status)
    if state == last_drawn_state:
        return

    display.fill(0)
    display.text("OmniEye", 0, 0)
    display.text("Level: {}".format(current_level), 0, 16)
    if current_distance is None:
        display.text("Dist: --", 0, 32)
    else:
        display.text("Dist: {:.2f}m".format(float(current_distance)), 0, 32)
    display.text(status, 0, 48)
    display.show()
    last_drawn_state = state


def handle_line(line):
    global current_distance, current_level, last_haptic_ms
    try:
        payload = json.loads(line)
    except ValueError:
        current_level = 0
        current_distance = None
        last_haptic_ms = None
        draw_status("Bad JSON")
        return

    if payload.get("type") != "haptic":
        return

    current_level = clamp_level(payload.get("level", 0))
    current_distance = payload.get("distance_m")
    last_haptic_ms = time.ticks_ms()
    draw_status("USB serial OK")


def poll_stdin():
    if poller.poll(0):
        line = sys.stdin.readline()
        if line:
            handle_line(line.strip())


while True:
    poll_stdin()
    if last_haptic_ms is None:
        draw_status("Waiting data")
    elif time.ticks_diff(time.ticks_ms(), last_haptic_ms) > TIMEOUT_MS:
        current_level = 0
        current_distance = None
        last_haptic_ms = None
        draw_status("Waiting data")
    time.sleep_ms(50)
