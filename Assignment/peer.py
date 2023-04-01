from Models.Peer import Peer
import threading
import os

port_no = int(input("Enter port number : "))
name = input("Peer number : ")

peer = Peer(port_no, "peer" + name + "/")

peer.join()

stop_flag = threading.Event()

def update_peer():
    while not stop_flag.is_set():
        # print("Updating peer")
        peer.update_peer();
    print("thread end")

def listen_to_peers():
    peer.listen_to_peers()

def ask_a_peer(file, port_no):
    peer.ask_a_peer(file, port_no)

def ask_peers(file):
    print("Request for file : ", file)
    peer.file_chunk = {}
    threads = []
    for p in peer.peer_list:
        if p != peer.port:
            t = threading.Thread(target=ask_a_peer, args=(file, p,))
            t.start()
            threads.append(t)
    
    # waiting till all threads append chunk info
    for t in threads:
        t.join()

    print("------FILE CHUNKS------")
    print(peer.file_chunk)
            

t1 = threading.Thread(target=update_peer)
t1.start()
t2 = threading.Thread(target=listen_to_peers)
t2.start()

while True:
    action = input("INPUT : ")
    if action.lower() == "close" or action.lower() == "c":
        print("Closing peer")
        stop_flag.set()
        peer.leave()
        os._exit(0)
        break
    
    if action.split(" ")[0].lower() == "ask":
        file = action.split(" ")[1]
        if not peer.check_if_file_exist(file):
            t = threading.Thread(target=ask_peers, args=(file,))
            t.start()
        else:
            print("File already exists")