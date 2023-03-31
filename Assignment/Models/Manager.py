import socket

class Manager:
    def __init__(self, port):
        # s is the server socekt object
        self.s = socket.socket()
        self.s.bind(('', port))
        self.s.listen(100)
        self.port = port
        self.peer_list = []
        print("Server started at port: ", port)

    def message_from_peer(self):
        pass

    def message_to_peer(self, conn, message):
        conn.send(message.encode())

    def send_peerlist(self):
        message = ""
        for _, port in self.peer_list:
            message += str(port) + ","
        for conn, _ in self.peer_list:
            self.message_to_peer(conn, message)

    def add_peer(self, c, port_no):
        self.peer_list.append((c, port_no))
        self.send_peerlist()
    
    def is_client_alive(self, conn):
        try:
            conn.sendall("ALIVE_CHECK".encode())
            conn.settimeout(2)
            response = conn.recv(1024)
            return True
        except:
            return False
        
    def check_peer(self):
        isModified = False
        for peer in self.peer_list:
            print("checking for ", peer[1])

            if not self.is_client_alive(peer[0]):
                
                print("Peer dead at port : ", peer[1])
                isModified = True
                self.peer_list.remove(peer)
        
        if isModified:
            self.send_peerlist()

    def __del__(self):
        # self.s.shutdown()
        self.s.close()
        print("Server closed")
