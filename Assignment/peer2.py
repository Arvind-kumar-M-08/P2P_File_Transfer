from Models.Peer import Peer
import threading
import os

peer = Peer()

peer.join()

stop_flag = threading.Event()

def update_peer():
    while not stop_flag.is_set():
        print("Updating peer")
        peer.update_peer();
    print("thread end")

t1 = threading.Thread(target=update_peer)
t1.start()

while True:
    action = input("INPUT : ")
    if action.lower() == "close":
            print("Closing peer")
            stop_flag.set()
            peer.leave()
            os._exit(0)
