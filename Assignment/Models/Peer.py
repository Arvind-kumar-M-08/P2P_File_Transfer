import socket
import os

class Peer:
    def __init__(self, port, folder, server_port = 10000):
        # s is the server socekt object
        self.s = socket.socket()
        self.s.connect(('127.0.0.1', server_port))
        self.peer_list = []

        #port for peer file transfer
        self.port = port
        self.peerSocket = socket.socket()
        self.peerSocket.bind(('', port))
        self.peerSocket.listen(100)
        print("Peer started")

        #data for file request
        self.file_chunk = {}
        self.folder = folder

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

    def listen_to_peers(self):
        while True:
            c, addr = self.peerSocket.accept()
            message = c.recv(1024).decode()
            print(message)
            c.close()

    def ask_a_peer(self, file, port_no):
        temps = socket.socket()
        temps.connect(('127.0.0.1', port_no))
        temps.send(("NEED "+ file).encode())
        message = temps.recv(1024).decode()
        
        temps.close()

    def check_if_file_exist(self, file):
        return os.path.isfile(self.folder + file)
    
    def __del__(self):
        # Closing the connection
        self.s.close()
        print("Peer closed")
    