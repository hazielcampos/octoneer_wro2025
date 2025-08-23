import time

is_running = False

def set_active(active: bool):
    global is_running
    is_running = active

def sleep(duration):
    global is_running
    duration = max(0.1, duration)  # Make sure duration is at least 0.1 seconds
    for _ in range(int(duration * 10)):
        if not is_running:
            break
        time.sleep(0.1)