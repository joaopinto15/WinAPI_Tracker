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

### 🧱 1. Build from Source (Developer Setup)

For advanced users or contributors who want to modify the tool.

#### ✅ Requirements

- Windows 10 or later
- Visual Studio (C++ workload)
- Python 3.8+ installed
- Pip packages:
  ```bash
  pip install frida pyinstaller
