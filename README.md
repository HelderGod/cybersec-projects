# Cybersecurity Tools

## 1. PortScanner

This is a simple port scanner that checks for open ports on a given IP address. It's useful for identifying running services on a target machine.

### How it works
1. The user enters one or multiple target IPs.
2. The script scans up to a specified number of ports.
3. If a port is open, it prints the result.

---

## 2. Remote Access Backdoor

This backdoor allows remote control over a compromised machine, featuring remote command execution, file transfer, screenshot capture, and keylogger.

### How it works
- `server.py` acts as the attacker's machine, listening for incoming connections.
- `backdoor.py` runs on the target machine and connects to the server.
- The attacker can send commands to control the target.

### Setup

1. **Important:** In both `server.py` and `backdoor.py`, replace the IP address with your server's IP.

3. **Network Setup:**  The attacker machine and the target machine **must be connected to the same network** for the connection to work properly. You can use a VM or physical machines, but they must be able to communicate via the same local network.

2. On the attacker's machine, start the server and wait for connections:
    ```bash
    python server.py
    ```

3. (Optional) If you want the Python file to be an executable for Windows, run this command:
    ```bash
    pyinstaller backdoor.py --onefile --noconsole
    ```
   Then execute the file from the `dist` folder.  
   Otherwise, you can run it through Python:
    ```bash
    python backdoor.py
    ```

---

## Available commands
- `quit`: Closes the connection.
- `cd <directory>`: Navigate through directories.
- `upload <filename>`: Uploads a file to the target.
- `download <filename>`: Downloads a file from the target.
- `screenshot`: Takes a screenshot of the target machine.
- `keylog_start`: Starts keylogging.
- `keylog_dump`: Retrieves recorded keystrokes.

---

## Disclaimer
This software is for educational purposes only. Unauthorized use is illegal.
