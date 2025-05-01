import frida
import sys
import json
import datetime
import os
import threading


base_dir = os.path.dirname(os.path.abspath(__file__))

SCRIPT_PATH = os.path.join(base_dir, "script.js")
OUTPUT_JSON = os.path.join(base_dir, "winAPI_log.json")

target_pid = None

def save_output():
    try:
        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[!] Error saving output: {e}")
# Make sure output directory exists
os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)

# Load or initialize the output array
if os.path.exists(OUTPUT_JSON):
    with open(OUTPUT_JSON, "r", encoding="utf-8") as f:
        try:
            output_data = json.load(f)
        except json.JSONDecodeError:
            output_data = []
else:
    output_data = []
    save_output()  # Create the file immediately

# Global stop event
stop_event = threading.Event()

def on_message(message, data):
    if message["type"] == "send":
        payload = message["payload"]
        timestamp = datetime.datetime.utcnow().isoformat()
        entry = {
            "timestamp": timestamp,
            "pid": target_pid,  # Add PID here
            "data": payload
        }

        print(f"[Frida] {entry}")
        output_data.append(entry)
        save_output()

    elif message["type"] == "error":
        print(f"[!] Script error: {message['stack']}")

def monitor_session(session):
    def on_detached(reason):
        print(f"[!] Detached from process: {reason}")
        stop_event.set()  # Stop the main thread

    session.on("detached", on_detached)

def main(pid):
    global target_pid
    target_pid = pid
    print(f"[+] Attaching to PID {target_pid}")
    session = frida.attach(target_pid)

    monitor_session(session)

    with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
        script_code = f.read()

    script = session.create_script(script_code)
    script.on("message", on_message)
    script.load()

    print("[+] Script loaded. Waiting for API calls...")
    try:
        stop_event.wait()  # Wait until detached
        print("[*] Exiting after target process termination.")
    except KeyboardInterrupt:
        print("[*] Interrupted. Detaching...")
        session.detach()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <pid>")
        sys.exit(1)

    try:
        pid = int(sys.argv[1])
        main(pid)
    except Exception as e:
        print(f"[!] Error: {e}")
        sys.exit(1)
