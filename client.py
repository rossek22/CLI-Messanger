import socket
import threading
import base64
import sys
import json
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from config import SECRET_KEY, SERVER_HOST, SERVER_PORT, CLIENT_LOCAL_PORT as CONFIG_CLIENT_LOCAL_PORT

try:
    import readline  # Для корректной работы в Linux/Unix
except ImportError:
    readline = None

SERVERS_FILE = 'servers.json'

# --- Вспомогательные функции для работы с серверами ---
def load_servers():
    if os.path.exists(SERVERS_FILE):
        with open(SERVERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_servers(servers):
    with open(SERVERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(servers, f, ensure_ascii=False, indent=2)

# --- Текстовое меню выбора сервера со стрелками ---
def select_server(servers):
    options = [
        ("new", "Ввести новый сервер"),
        ("config", f"Использовать значения из config.py ({SERVER_HOST}:{SERVER_PORT}, local: {CONFIG_CLIENT_LOCAL_PORT})")
    ]
    for i, s in enumerate(servers):
        label = f"{s['host']}:{s['port']} (local: {s['local_port']})"
        options.append((str(i), label))

    print("Выберите сервер для подключения:")
    for idx, (_, label) in enumerate(options):
        print(f"  {idx}. {label}")
    print("\nВведите номер нужного пункта и нажмите Enter (например, 1):")

    while True:
        sel = input("Ваш выбор: ").strip()
        if sel.isdigit():
            idx = int(sel)
            if 0 <= idx < len(options):
                value = options[idx][0]
                if value == 'new':
                    return None
                if value == 'config':
                    return {'host': SERVER_HOST, 'port': SERVER_PORT, 'local_port': CONFIG_CLIENT_LOCAL_PORT}
                if value.isdigit() and 0 <= int(value) < len(servers):
                    return servers[int(value)]
        print("Некорректный ввод. Попробуйте снова.")

# --- Ввод параметров сервера ---
def input_server():
    host = input("IP сервера (например, 127.0.0.1): ").strip()
    while not host:
        host = input("IP сервера (например, 127.0.0.1): ").strip()
    port = input("Порт сервера (например, 5552): ").strip()
    while not port.isdigit():
        port = input("Порт сервера (например, 5552): ").strip()
    local_port = input("Локальный порт клиента (Enter = авто): ").strip()
    if local_port == '':
        local_port = None
    else:
        try:
            local_port = int(local_port)
        except ValueError:
            local_port = None
    return {'host': host, 'port': int(port), 'local_port': local_port}

# --- Сохранение сервера ---
def ask_save_server(server, servers):
    ans = input("Сохранить сервер? (Y/N): ").strip().lower()
    if ans == 'y':
        if server not in servers:
            servers.append(server)
            save_servers(servers)
            print("Сервер сохранён!")
        else:
            print("Такой сервер уже есть в списке.")

# --- Основная логика ---
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
    servers = load_servers()
    server = select_server(servers)
    if server is None:
        server = input_server()
        ask_save_server(server, servers)

    HOST = server['host']
    PORT = server['port']
    CLIENT_LOCAL_PORT = server['local_port']

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
                msg = decrypt_message(data)
                # Фикс: выводим входящее сообщение на новой строке, не мешая вводу
                if readline:
                    saved_line = readline.get_line_buffer()
                    sys.stdout.write('\r' + ' ' * (len(saved_line) + 2) + '\r')
                    print(msg)
                    sys.stdout.write(f"> {saved_line}")
                    sys.stdout.flush()
                else:
                    # Windows: просто печатаем с новой строки
                    print(f"\r{msg}\n> ", end="", flush=True)
            except:
                break

    thread = threading.Thread(target=listen)
    thread.daemon = True
    thread.start()

    while True:
        try:
            msg = input('> ')
        except EOFError:
            break
        if not msg:
            continue
        full_msg = f"{nickname}: {msg}"
        client.send(encrypt_message(full_msg))

if __name__ == "__main__":
    main()
