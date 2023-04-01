import socket

class Peer:
    def __init__(self, port, server_port = 10000):
        # s is the server socekt object
        self.s = socket.socket()
        self.s.connect(('127.0.0.1', server_port))
        self.peer_list = []

        #port for peer file transfer
        self.port = port
        print("Peer started")

    def join(self):
        # sending HI for new peer
        self.s.send(("HI " + str(self.port)).encode())

    # always checking for active peers
    def update_peer(self):
        message = self.s.recv(1024).decode()
        if len(message) > 0:
            if message == "ALIVE_CHECK":
                self.s.send("OK".encode())
                return
            message = message[:-1]
            message = message.split(',')
            self.peer_list = [int(i) for i in message]
            print(self.peer_list)
    def leave(self):
        print("Sending bye message")
        message = "BYE"
        self.s.send(message.encode())

    def __del__(self):
        # Closing the connection
        self.s.close()
        print("Peer closed")
    