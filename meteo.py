import socketserver
import datetime
import requests


class MyTCPSocketHandler(socketserver.BaseRequestHandler):
    def handle(self):
        res = requests.get(
            "https://api.openweathermap.org/data/2.5/weather?q=Modena&appid=$$")

        data = res.json()
        temp = (float(data['main']['temp']) - 273.15).__round__(4)
        desc = data['weather'][0]['description']

        self.request.sendall(
            f'Temperature: {temp}°C, description: {desc}'.encode())


if __name__ == "__main__":
    HOST, PORT = "localhost", 2002

    server = socketserver.TCPServer((HOST, PORT), MyTCPSocketHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("server closing")
        server.server_close()
