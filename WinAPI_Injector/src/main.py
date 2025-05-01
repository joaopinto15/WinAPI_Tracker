import os
import sys

from config_loader import get_config_log_path
from output_logger import OutputLogger
from frida_controller import start_monitoring

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <pid>")
        sys.exit(1)

    try:
        pid = int(sys.argv[1])
    except ValueError:
        print("[!] Invalid PID")
        sys.exit(1)

    base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    script_path = os.path.join(base_dir, "script.js")
    output_path = get_config_log_path(base_dir)
    logger = OutputLogger(output_path)

    start_monitoring(pid, script_path, logger)

if __name__ == "__main__":
    main()
