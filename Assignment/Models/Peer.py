import socket

class Peer:
    def __init__(self, server_port = 10000):
        # s is the server socekt object
        self.s = socket.socket()
        self.s.connect(('127.0.0.1', server_port))
        self.peer_list = []
        print("Peer started")

    def __del__(self):
        self.s.close()
        print("Peer closed")
    