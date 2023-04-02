"""Manager Class for peer-peer application"""
import socket

class Manager:
    """
    A class that defines a server that listens for incoming connections from peers and keeps track of them.

    Attributes:
    -----------
    s : socket.socket
        The server socket object.
    port : int
        The port on which the server is listening.
    peer_list : list
        A list of tuples representing the connected peers. Each tuple contains a connection object, 
        the IP address and port number of the peer.
    last_broadcasted : list
        A copy of the last broadcasted peer list.        
    """

    def __init__(self, port):
        """
        Initializes the server socket object, binds it to the given port, and starts listening for connections.
        """
        self.s = socket.socket()
        self.s.bind(('', port))
        self.s.listen(100)
        self.port = port
        self.peer_list = []

        self.last_broadcasted = []
        print("-------------------------------------")
        print("Server started at port: ", port)
        print("Enter close or c to close the server")
        print("-------------------------------------")

    def message_to_peer(self, conn, message):
        """
        Sends the given message to the peer over the given connection.

        Args:
            conn (socket connection obj): socket connection object of peer
            message (str): message to be sent
        """
        conn.send(message.encode())

    # Broadcasting peer list
    def send_peerlist(self):
        """
        Broadcasts the current list of connected peers to all connected peers.
        """
        self.last_broadcasted = list(self.peer_list)
        message = ""
        for _, cur, peer_port in self.peer_list:
            message += cur[0] + ","
            message += str(peer_port) + ","
        for conn, cur_port ,_ in self.peer_list:
            try:
                self.message_to_peer(conn, message)
            except (ConnectionResetError, ConnectionAbortedError, TimeoutError):
                print("Error while sending message to ", cur_port)
                
    def __del__(self):
        """
        Closes the server socket object and prints a message indicating that the server has been closed.
        """
        self.s.close()
        print("Server closed")
