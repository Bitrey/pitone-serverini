import socketserver
import datetime


class MyTCPSocketHandler(socketserver.BaseRequestHandler):
    def handle(self):
        date = datetime.datetime.today().strftime('%d/%m/%Y')
        self.request.sendall(date.encode())


if __name__ == "__main__":
    HOST, PORT = "localhost", 2001

    server = socketserver.TCPServer((HOST, PORT), MyTCPSocketHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("server closing")
        server.server_close()
