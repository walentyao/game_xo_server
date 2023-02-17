from simple_websocket_server import WebSocketServer, WebSocket


class Server(WebSocket):
    def handle(self):
        print(self.data)
        for client in clients:
            if client != self:
                client.send_message(self.data)

    def connected(self):
        print(self.address, 'connected')
        # for client in clients:
        #     client.send_message(self.address[0] + u' - connected')
        clients.append(self)

    def handle_close(self):
        clients.remove(self)
        print(self.address, 'closed')
        for client in clients:
            client.send_message('disconnected')


clients = []

server = WebSocketServer('', 8000, Server)
server.serve_forever()
