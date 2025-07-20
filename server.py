import socket
import threading
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from config import SECRET_KEY, SERVER_PORT


HOST = '0.0.0.0'
clients = []

print("KEY BYTES =", SECRET_KEY, "LEN =", len(SECRET_KEY))
assert len(SECRET_KEY) == 32, "Ключ НЕ 32 байта!"


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

def broadcast(message, conn):
    for client in clients:
        if client != conn:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

def handle_client(conn, addr):
    print(f"[+] Подключился {addr}")
    while True:
        try:
            data = conn.recv(2048)
            if not data:
                break
            
            broadcast(data, conn)
        except:
            break
    print(f"[-] {addr} отключился")
    clients.remove(conn)
    conn.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, SERVER_PORT))
    server.listen()
    print(f"[SERVER] Запущен на {HOST}:{SERVER_PORT}")

    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()
