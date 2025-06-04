███╗   ██╗███████╗████████╗  ██╗  ██╗██╗████████╗
████╗  ██║██╔════╝╚══██╔══  ╝██║ ██╔╝██║╚══██╔══╝
██╔██╗ ██║█████╗     ██║     █████╔╝ ██║   ██║   
██║╚██╗██║██╔══╝     ██║     ██╔═██╗ ██║   ██║   
██║ ╚████║███████╗   ██║     ██║  ██╗██║   ██║   
╚═╝  ╚═══╝╚══════╝   ╚═╝      ╚═╝  ╚═╝╚═╝   ╚═╝  
                  N E T K I T
               A Netcat clone in Python

NetKit is a Python-based Netcat clone designed to provide basic networking tools such as remote shell access, file transfers, and simple TCP/UDP communication.

![Python](https://img.shields.io/badge/Made%20with-Python-blue?logo=python)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow)

---

## 📌 Features (Planned)
- ✅ TCP client and listener mode
- ⏳ Reverse shell support
- ⏳ File transfer over socket
- ⏳ Simple shell command execution on remote host
- ⏳ UDP support (optional in future)

---

## 📦 Requirements

- Python 3.6+
- No external libraries (uses only standard library)

---

## 🚀 Usage

```bash
# Start listener mode (e.g., like `nc -lvp 4444`)
python netkit.py --listen --port 4444

# Connect to a remote host
python netkit.py --target 192.168.1.10 --port 4444