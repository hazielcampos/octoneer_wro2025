is_running = False

FREE_TEST = 0
OBSTACLE_TEST = 1

mode = FREE_TEST
pid_error = 0.0

def set_is_running(status):
    global is_running
    is_running = status

def set_error(error):
    global pid_error
    pid_error = error