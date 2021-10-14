import socketserver
import json
import datetime


class MyTCPSocketHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).decode().strip()

        data = None
        with open('orari.json') as f:
            data = json.load(f)

        giorno_attuale = datetime.datetime.today().weekday() + 1
        ora_attuale = now = datetime.datetime.now().hour

        materie: list[tuple[int, int, str]] = []  # (da, a, nome)
        for materia in data:
            for ora in materia['ore']:
                if ora['giorno'] == giorno_attuale:
                    materie.append((ora['da'], ora['a'], materia['nome']))

        materie = sorted(materie, key=lambda x: x[0])
        _materie = materie[:]
        _materie.reverse()

        materia_attuale = None
        for m in _materie:
            if m[0] == ora_attuale or ora_attuale < m[1]:
                materia_attuale = m[2]

        final_str = "Oggi abbiamo\n" + '\n'.join([
            f'Dalle {da} alle {a}: {nome}' for da, a, nome in materie
        ])
        final_str += f'\nAdesso abbiamo {materia_attuale}'

        print("received", self.data)

        self.request.sendall(final_str.encode())


if __name__ == "__main__":
    HOST, PORT = "localhost", 2003

    server = socketserver.TCPServer((HOST, PORT), MyTCPSocketHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("server closing")
        server.server_close()
