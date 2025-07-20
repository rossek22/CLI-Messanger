import socket
import threading
import base64
import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from config import SECRET_KEY, SERVER_HOST, SERVER_PORT, CLIENT_LOCAL_PORT as CONFIG_CLIENT_LOCAL_PORT

# HOST и PORT по умолчанию
HOST = SERVER_HOST
PORT = SERVER_PORT
CLIENT_LOCAL_PORT = CONFIG_CLIENT_LOCAL_PORT

# Переопределение через аргументы командной строки
if len(sys.argv) > 1:
    HOST = sys.argv[1]
if len(sys.argv) > 2:
    PORT = int(sys.argv[2])
if len(sys.argv) > 3:
    CLIENT_LOCAL_PORT = int(sys.argv[3])


def encrypt_message(message: str) -> bytes:
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    return base64.b64encode(cipher.iv + ct_bytes)

def decrypt_message(enc_message: bytes) -> str:
    raw = base64.b64decode(enc_message)
    iv = raw[:16]
    ct = raw[16:]
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct), AES.block_size).decode()

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if CLIENT_LOCAL_PORT is not None:
        client.bind(("", CLIENT_LOCAL_PORT))
    client.connect((HOST, PORT))
    print(f"[+] Подключено к серверу {HOST}:{PORT}! (локальный порт: {client.getsockname()[1]})")
    
    nickname = input("Введи свой никнейм: ")
    print(f"Твой ник: {nickname}")

    def listen():
        while True:
            try:
                data = client.recv(2048)
                if not data:
                    break
                print(decrypt_message(data))
            except:
                break

    thread = threading.Thread(target=listen)
    thread.daemon = True
    thread.start()

    while True:
        msg = input()
        if not msg:
            continue
        full_msg = f"{nickname}: {msg}"
        client.send(encrypt_message(full_msg))

if __name__ == "__main__":
    main()
