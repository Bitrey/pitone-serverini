import socketserver
import datetime
import requests


class MyTCPSocketHandler(socketserver.BaseRequestHandler):
    def handle(self):
        dict_dns = {
            'date': ("localhost", 2001),
            'meteo': ("localhost", 2002),
            'timetable': ("localhost", 2003)
        }
        self.data = self.request.recv(1024).decode().strip()
        if self.data in dict_dns:
            string_to_send = f'{dict_dns[self.data][0]};{dict_dns[self.data][1]}'
            self.request.sendall(string_to_send.encode())
        else:
            self.request.sendall('NOTFOUND'.encode())

        print("received", self.data)


if __name__ == "__main__":
    HOST, PORT = "localhost", 2000

    server = socketserver.TCPServer((HOST, PORT), MyTCPSocketHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("server closing")
        server.server_close()
