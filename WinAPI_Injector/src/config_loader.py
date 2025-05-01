import configparser
import os
import sys

def get_config_log_path(base_dir):
    config = configparser.ConfigParser()
    config_path = os.path.join(base_dir, "config.ini")
    config.read(config_path)
    try:
        return config["monitor"]["log_file_path"]
    except KeyError:
        print("[!] Failed to read log_file_path from config.ini")
        sys.exit(1)
