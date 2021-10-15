import socket
import sys
import json
import os


def load_json():
    if not os.path.exists('cache.json'):
        with open('cache.json', 'w') as f:
            f.write("[]")
    with open('cache.json') as f:
        data = json.load(f)
        return data


def load_url(name: str):
    json_cache = load_json()
    return json_cache[name] if name in json_cache else None


arg = " ".join(sys.argv[1:])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dns_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if not arg:
    print('arg not given')
    sys.exit()

try:
    HOST = None
    PORT = None
    DNS_SERVER_ADDR = (('localhost', 2000))

    if arg in load_json():
        # print(f'"{arg}" is saved in cache')

        obj = load_url(arg)
        HOST = obj['addr']
        PORT = obj['port']
    else:
        # print(f'"{arg}" is not saved in cache')

        dns_sock.connect(DNS_SERVER_ADDR)
        dns_sock.sendall(arg.encode())

        received = dns_sock.recv(1024).decode()
        dns_sock.close()

        # print('dns server sent ' + received)

        if received == 'NOTFOUND':
            print('server unreacheable')
        else:
            HOST = received.split(';')[0]
            PORT = int(received.split(';')[1])

            cache = load_json()
            cache[arg] = {
                'addr': HOST,
                'port': PORT
            }
            with open('cache.json', 'w', encoding='utf-8') as f:
                json.dump(cache, f, ensure_ascii=False, indent=4)

        # print(f'dns server sent {HOST}:{str(PORT)}')

    if HOST is None:
        print('can\'t connect to server')
    else:
        # print(f'connecting to socket {HOST}:{str(PORT)}')
        sock.connect((HOST, PORT))
        # print('connected, waiting for a response')
        received = sock.recv(1024).decode()
        print(f'received: {received}')
except KeyboardInterrupt:
    print('ctrl+c')
    sock.close()
except (ConnectionAbortedError, ConnectionResetError):
    print('connection lost')
    sock.close()
except ConnectionRefusedError:
    print('connection refused, is the server up?')
    sock.close()
finally:
    print('closing client')
    sock.close()
