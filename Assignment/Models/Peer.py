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
        self.received_file = {}
        self.file_size = 0
        self.file_chunk = []
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
            message = message.split(" ")
            
            #Asking file chunk
            if message[0] == "NEED":
                print(message)
                sending = ""
                if self.check_if_file_exist(message[1]):
                    sending = "YES " + str((os.path.getsize(self.folder + message[1]) + 1023)//1024)
                    # sending = self.has_chunks(message[1])
                else:
                    sending = "NO"
                
                c.send(sending.encode())
            if message[0] == "SEND":
                print(message)
                if self.check_if_file_exist(message[1]):
                    sending = self.get_chunk_from_file(message[1], int(message[2]))
                
                if len(sending):
                    c.send(sending)
            c.close()
    
    def get_chunk_from_file(self, file, chunk_no):
        f = open(self.folder + file, "rb")
        _ = f.read(1024*chunk_no)
        message = f.read(1024)
        if not message:
            return ""
        return message

    def ask_a_peer(self, file, port_no):
        try:
            self.file_chunk= []
            temps = socket.socket()
            temps.connect(('127.0.0.1', port_no))
            temps.send(("NEED "+ file).encode())
            message = temps.recv(1024).decode()
            print(message)
            message = message.split(" ")

            #YES
            if message[0] == "YES":
                self.file_size = int(message[1])
                self.file_chunk.append(port_no)
            
            temps.close()
        except:
            print("No peer found : ", port_no)

            
    def request_chunk(self, file, port_no, chunk_no):
        try:
            temps = socket.socket()
            temps.connect(('127.0.0.1', port_no))
            temps.send(("SEND "+ file + " " + str(chunk_no)).encode())
            message = temps.recv(1024)
            # print(message)
            # print("Received chunk for file : ", file," ",chunk_no)
            self.received_file[chunk_no] = message
            
            temps.close()
        except:
            print("No peer found : ", port_no)

    def add_file_to_folder(self, file):
        f = open(self.folder + file, "wb")
        for i in range(self.file_size):
            f.write(self.received_file[i])
        f.close()

        if os.path.isfile(self.folder + file):
            print("Added ", file, " to the folder ", self.folder)
        else:
            print("Error in adding file : ", file)
    def check_if_file_exist(self, file):
        return os.path.isfile(self.folder + file)
    
    def __del__(self):
        # Closing the connection
        self.s.close()
        print("Peer closed")
    