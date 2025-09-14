import threading
from enum import Enum
from colorama import Fore, Style, init
from datetime import datetime
from pathlib import Path
import shutil

init(autoreset=True)
logger = None
lock = threading.Lock()

class LogType(Enum):
    ERROR = 1
    WARN = 2
    INFO = 3

class Logger:
    def __init__(self, log_dir="./logs/"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.latest_file = self.log_dir / "latest.log"

        # Si existe latest.log, renombrarlo usando el header datetime
        if self.latest_file.exists():
            with open(self.latest_file, "r") as f:
                first_line = f.readline().strip()
            
            # Extraer datetime del header: "[2025-09-14 10:00:00] Log started"
            if first_line.startswith("[") and "]" in first_line:
                timestamp_str = first_line.split("]")[0][1:]
                try:
                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
                except ValueError:
                    timestamp = datetime.now()
            else:
                timestamp = datetime.now()

            new_name = self.log_dir / f"{timestamp.strftime('%Y-%m-%d_%H-%M-%S')}.log"
            shutil.move(self.latest_file, new_name)

        # Crear un nuevo latest.log con header
        with open(self.latest_file, "w") as f:
            header = f"[{datetime.now()}] Log started\n"
            f.write(header)

    def _write(self, msg: str, color: str):
        text = f"[{datetime.now()}] {msg}"
        print(color + text)
        with lock:
            with open(self.latest_file, "a") as f:
                f.write(f"{text}\n")

    def Error(self, msg: str):
        self._write(f"[ERROR] {msg}", Fore.RED)

    def Info(self, msg: str):
        self._write(f"[INFO] {msg}", Fore.CYAN)

    def Warn(self, msg: str):
        self._write(f"[WARN] {msg}", Fore.YELLOW)

def get_logger():
    global logger
    if not logger:
        logger = Logger()
    return logger
