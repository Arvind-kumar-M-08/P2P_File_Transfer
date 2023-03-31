import socket

class Peer:
    def __init__(self, server_port = 10000):
        # s is the server socekt object
        self.s = socket.socket()
        self.s.connect(('127.0.0.1', server_port))
        self.peer_list = []

        print("Peer started")

    def join(self):
        # sending HI for new peer
        self.s.send("HI".encode())

    def update_peer(self):
        while True:
            message = self.s.recv(1024).decode()
            if len(message):
                message = message[:-1]
                message = message.split(',')
                self.peer_list = message
                print(self.peer_list)

    def __del__(self):
        self.s.close()
        print("Peer closed")
    