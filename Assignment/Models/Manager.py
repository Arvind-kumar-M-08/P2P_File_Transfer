"""Manager Class for peer-peer application"""
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

    # Broadcasting peer list
    def send_peerlist(self):
        message = ""
        for _,_, port in self.peer_list:
            message += str(port) + ","
        for conn, _ ,_ in self.peer_list:
            try:
                self.message_to_peer(conn, message)
            except:
                pass
                
    def __del__(self):
        # self.s.shutdown()
        self.s.close()
        print("Server closed")
