from Models.Peer import Peer
import threading

peer = Peer()

peer.join()



def update_peer():
    peer.update_peer();


t1 = threading.Thread(target=update_peer)
t1.start()

while True:
    pass


