# CLI Messenger (Python, AES)

Простой CLI-мессенджер на Python с шифрованием сообщений (AES-256, CBC). Поддерживает несколько клиентов, централизованную настройку через config.py и передачу сообщений по сети.

## Возможности
- Передача сообщений между клиентами через сервер
- Шифрование сообщений (AES-256, CBC, pycryptodome)
- Централизованная настройка ключа, адреса и портов в `config.py`
- Возможность указания адреса и портов через аргументы командной строки

## Установка
1. Клонируйте репозиторий
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## Настройка
Откройте файл `config.py` и укажите параметры:

```python
SECRET_KEY = b'ваш_секретный_32_байтный_ключ'  # 32 байта!
SERVER_HOST = '127.0.0.1'  # Адрес сервера по умолчанию
SERVER_PORT = 5552         # Порт сервера
CLIENT_LOCAL_PORT = None   # Локальный порт клиента (None = автоназначение, либо укажите порт, например, 6000)
```

- **SECRET_KEY** — обязательно 32 байта (256 бит)
- **SERVER_HOST** — адрес сервера (для клиента)
- **SERVER_PORT** — порт, на котором работает сервер
- **CLIENT_LOCAL_PORT** — локальный порт клиента (опционально)

## Запуск

### Сервер
```bash
python server.py
```

### Клиент
```bash
python client.py [server_host] [server_port] [client_local_port]
```
- `server_host` — адрес сервера (по умолчанию из config.py)
- `server_port` — порт сервера (по умолчанию из config.py)
- `client_local_port` — локальный порт клиента (по умолчанию из config.py или автоназначение)

**Примеры:**
- Подключиться к серверу по умолчанию:
  ```bash
  python client.py
  ```
- Подключиться к серверу 192.168.1.10:5552 с локального порта 6000:
  ```bash
  python client.py 192.168.1.10 5552 6000
  ```

## Принцип работы
- Сервер принимает подключения клиентов и пересылает сообщения между ними.
- Все сообщения шифруются на клиенте и расшифровываются на клиенте.
- Сервер не расшифровывает сообщения, а только пересылает их.

## Требования
- Python 3.7+
- pycryptodome

## Безопасность
- Используйте уникальный и сложный SECRET_KEY (32 байта)
- Не используйте ключ по умолчанию в продакшене

## Лицензия
GPL

---

# CLI Messenger (Python, AES) [EN]

A simple CLI messenger in Python with AES-256 (CBC) encryption. Supports multiple clients, centralized configuration via `config.py`, and message transfer over the network.

## Features
- Message transfer between clients via server
- Message encryption (AES-256, CBC, pycryptodome)
- Centralized configuration of key, address, and ports in `config.py`
- Ability to specify address and ports via command-line arguments

## Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
Open `config.py` and set the parameters:

```python
SECRET_KEY = b'your_secret_32_byte_key'  # 32 bytes!
SERVER_HOST = '127.0.0.1'  # Default server address
SERVER_PORT = 5552         # Server port
CLIENT_LOCAL_PORT = None   # Client local port (None = auto, or specify e.g. 6000)
```

- **SECRET_KEY** — must be exactly 32 bytes (256 bits)
- **SERVER_HOST** — server address (for client)
- **SERVER_PORT** — port the server listens on
- **CLIENT_LOCAL_PORT** — client local port (optional)

## Usage

### Server
```bash
python server.py
```

### Client
```bash
python client.py [server_host] [server_port] [client_local_port]
```
- `server_host` — server address (default from config.py)
- `server_port` — server port (default from config.py)
- `client_local_port` — client local port (default from config.py or auto)

**Examples:**
- Connect to default server:
  ```bash
  python client.py
  ```
- Connect to 192.168.1.10:5552 from local port 6000:
  ```bash
  python client.py 192.168.1.10 5552 6000
  ```

## How it works
- The server accepts client connections and relays messages between them.
- All messages are encrypted and decrypted on the client side.
- The server does not decrypt messages, it only relays them.

## Requirements
- Python 3.7+
- pycryptodome

## Security
- Use a unique and strong SECRET_KEY (32 bytes)
- Do not use the default key in production

## License
GPL
