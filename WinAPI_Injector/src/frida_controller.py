import frida
import datetime
import threading

stop_event = threading.Event()
target_pid = None  # Used globally within this module

def on_message(message, data, output_logger):
    if message["type"] == "send":
        payload = message["payload"]
        timestamp = datetime.datetime.utcnow().isoformat()
        entry = {
            "timestamp": timestamp,
            "pid": target_pid,
            "data": payload
        }
        print(f"[Frida] {entry}")
        output_logger.append(entry)

    elif message["type"] == "error":
        print(f"[!] Script error: {message['stack']}")

def monitor_session(session):
    def on_detached(reason):
        print(f"[!] Detached from process: {reason}")
        stop_event.set()
    session.on("detached", on_detached)

def start_monitoring(pid, script_path, output_logger):
    global target_pid
    target_pid = pid
    print(f"[+] Attaching to PID {pid}")
    session = frida.attach(pid)
    monitor_session(session)

    with open(script_path, "r", encoding="utf-8") as f:
        script_code = f.read()

    script = session.create_script(script_code)
    script.on("message", lambda m, d: on_message(m, d, output_logger))
    script.load()

    print("[+] Script loaded. Waiting for API calls...")
    try:
        stop_event.wait()
        print("[*] Exiting after target process termination.")
    except KeyboardInterrupt:
        print("[*] Interrupted. Detaching...")
        session.detach()
