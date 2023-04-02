"""Peer Class for peer-peer application"""
import os
import socket

class Peer:
    """
    A class that defines a peer that connects to manager and get active peer list.
    Listens to all peers and sends file chunk on request.

    Attributes:
    -----------
    s : socket.socket
        The server socket object.
    port : int
        The port on which it is listening for other peers.
    peer_list : list
        A list of tuples representing the connected peers. Each tuple contains a
        the IP address and port number of the peer.
    shareable_files : list
        A list of all files available for sharing
    folder : str
        Folder where files are stored  
    """

    def __init__(self, port, folder, server_ip = '127.0.0.1' ,server_port = 10000):
        """
        Initializes the peer socket object, binds it to the given port, and starts listening for peers.
        """
        self.s = socket.socket()
        self.ip = socket.gethostbyname(socket.gethostname())
        self.s.connect((server_ip, server_port))

        # list of tuple (ip, port)
        self.peer_list = []
        self.folder = folder

        if not os.path.isdir(self.folder):
            os.mkdir(self.folder)

        #List of shareable files
        self.shareable_files = os.listdir(self.folder)

        #port for peer file transfer
        self.port = port
        self.peer_socket = socket.socket()
        self.peer_socket.bind(('', port))
        self.peer_socket.listen(100)

        #data for file request
        self.received_file = {}
        self.file_size = 0
        self.file_chunk = []
        
        print("\t\t---------------------------")
        print("\t\tPeer started")
        print("\t\tUse the following")
        print("\t\t1 -> Requesting a file")
        print("\t\t2 -> Shareable files")
        print("\t\t3 -> List of active peers")
        print("\t\t4 -> Exit")
        print("\t\t---------------------------")

    def join(self):
        """
        Connects with the manager on starting. Sends "HI port_no"
        """
        self.s.send(("HI " + str(self.port)).encode())

    # always checking for active peers
    def update_peer(self):
        """
        Updates the peer list and sends OK when manager checks connectivity
        """
        message = self.s.recv(1024).decode()
        if len(message) > 0:
            if message == "ALIVE_CHECK":
                self.s.send("OK".encode())
                return
            message = message[:-1]
            message = message.split(',')
            self.peer_list = []
            for i in range(0, len(message), 2):
                self.peer_list.append((message[i], int(message[i+1])))

    def leave(self):
        """
        Sends BYE message to the manager before leaving
        """
        message = "BYE"
        self.s.send(message.encode())

    def listen_to_peers(self):
        """
        Listens to other peers. Responds "YES file_size_in_chunks" for "NEED" if the file is available otherwise sends "NO".
        Sends the asked chunk for "SEND" request
        """
        while True:
            c, addr = self.peer_socket.accept()
            message = c.recv(1024).decode()
            message = message.split(" ")
            
            #Asking file chunk
            if message[0] == "NEED":
                sending = ""
                if self.check_if_file_exist(message[1]):
                    sending = "YES " + str((os.path.getsize(self.folder + message[1]) + 1023)//1024)
                    # sending = self.has_chunks(message[1])
                else:
                    sending = "NO"
                
                c.send(sending.encode())
            if message[0] == "SEND":
                if self.check_if_file_exist(message[1]):
                    sending = self.get_chunk_from_file(message[1], int(message[2]))
                
                if len(sending):
                    c.send(sending)
            c.close()
 
    def get_chunk_from_file(self, file, chunk_no):
        """
        Gets the required chunk (index) from the file. Each chunk is of 1024 bytes. INdexing starts from 0.

        Args:
            file (str) : filename to get the chunk from
            chunk_no (int) : chunk index
        """
        f = open(self.folder + file, "rb")
        useless = f.read(1024*chunk_no)
        message = f.read(1024)
        if not message:
            return ""
        return message

    def ask_a_peer(self, file, peer):
        """
        Asks if the peer has that file

        Args:
            file (str) : filename
            peer (tuple(str, int)) : (ip address, portno)
        """
        try:
            self.file_chunk= []
            temps = socket.socket()
            temps.connect((peer[0], peer[1]))
            temps.send(("NEED "+ file).encode())
            message = temps.recv(1024).decode()
            message = message.split(" ")

            #YES
            if message[0] == "YES":
                self.file_size = int(message[1])
                self.file_chunk.append(peer)
            
            temps.close()
        except (socket.error, ConnectionRefusedError, ConnectionResetError, TimeoutError):
            print("Peer connection error at : ", peer)

            
    def request_chunk(self, file, peer, chunk_no):
        """
        Request the required chunk to a selected peer

        Args:
            file (str) : filename
            peer (tuple(str, int)) : (ip address, portno)
            chunk_no (int) : index of the chunk
        """
        try:
            temps = socket.socket()
            temps.connect((peer[0], peer[1]))
            temps.send(("SEND "+ file + " " + str(chunk_no)).encode())
            message = temps.recv(1024)
            self.received_file[chunk_no] = message
            
            temps.close()
        except (socket.error, ConnectionRefusedError, ConnectionResetError, TimeoutError):
            print("Peer connection error at : ", peer)

    def add_file_to_folder(self, file):
        """
        Adds the file to the folder and list of shareable files

        Args:
            file (str) : filename
        """
        f = open(self.folder + file, "wb")
        for i in range(self.file_size):
            f.write(self.received_file[i])
        f.close()

        if os.path.isfile(self.folder + file):
            self.shareable_files.append(file)
            print("Added ", file, " to the folder ", self.folder)
        else:
            print("Error in adding file : ", file)
        
    def check_if_file_exist(self, file):
        """
        Checks if the file is available in the list

        Args:
            file (str) : filename
        """
        return file in self.shareable_files
    
    def __del__(self):
        """
        Closes the peer socket object and prints a message indicating that the peer has been closed.
        """
        self.s.close()
        print("Peer closed")
    