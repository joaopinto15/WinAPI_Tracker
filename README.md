# 🛡️ Process Monitor with ETW and Frida

A Windows-based background service that monitors real-time process creation using **ETW (Event Tracing for Windows)** and injects a **Frida** script into suspicious processes to hook and log WinAPI calls. Designed for malware analysis, threat detection, and behavioral monitoring.

---

## 🔍 Features

- Real-time monitoring of process creation via ETW
- Detects suspicious execution paths and PPID spoofing
- Automatically injects a Frida-based API hooker into targets
- Logs WinAPI calls to structured JSON
- Dynamic path resolution (no hardcoded folders)
- Can run silently as a service or background task

---

## 📦 Installation Options

### 💻 1. Precompiled Executable (User Setup)

Download the latest release from the [Releases](https://github.com/joaopinto15/WinAPI_Tracker/releases) page and extract it.

To run the monitor:

> ✅ Simply execute the `process_monitor.exe` in the **same folder** as the `injector.exe`.

No additional setup is required.

### 🧱 2. Build from Source (Developer Setup)

For advanced users or contributors who want to modify the tool.

Here’s the corrected and properly formatted version of that section in Markdown:

#### ✅ Requirements

- Windows 10 or later  
- Visual Studio (C++ workload)  
- Python 3.8+ installed  
- Required Python packages:

```bash
pip install frida pyinstaller
```

---

### 🏗️ Build the Standalone Executable

Use the provided `injector.spec` file to build the Python component with PyInstaller:

```bash
pyinstaller injector.spec
```

---

### ⚙️ Configuration

Edit the `config.ini` file to specify where logs should be saved:

```ini
[monitor]
log_file_path = logs/output.json
```

The path is resolved dynamically at runtime.

---

### 📊 Output Format

Each API call hook is logged as a structured JSON object:

```json
{
  "timestamp": "2025-05-01T23:18:53.152446",
  "process_name": "example.exe",
  "pid": 17696,
  "data": [
    "CreateThread",
    "..."
  ]
}
```

### 🎥 Demo

A short screen recording showing real-time process detection, Frida injection, and WinAPI logging in action.

![Process Monitor Demo](./gif.gif)
