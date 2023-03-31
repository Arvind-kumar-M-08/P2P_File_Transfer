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

    def message_to_peer(self, port_no):
        pass

    def __del__(self):
        # self.s.shutdown()
        self.s.close()
        print("Server closed")
