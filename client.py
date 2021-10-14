import socket
import sys
import json
import os


def load_json():
    if not os.path.exists('cache.json'):
        with open('cache.json', 'w') as f:
            f.write("[]")
    f = open('cache.json')
    data = json.load(f)
    f.close()
    return data


def load_url(name: str):
    try:
        return load_json()[next(i for i, d in enumerate(load_json()) if name in d)][name]
    except Exception:
        return None


arg = " ".join(sys.argv[1:])

# create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    obj = load_url(arg)
    if obj is None:
        print(f'{arg} doesn\'t exist')
        raise Exception("not found")

    HOST = obj["addr"]
    PORT = obj["port"]

    # connect to server
    sock.connect((HOST, PORT))

    # send arg
    sock.sendall((arg + "\n").encode())

    # receive arg back from the server
    received = sock.recv(1024).decode()
    print(f'Ricevuto: {received}')

except Exception:
    sock.close()
finally:
    # shut down
    sock.close()
