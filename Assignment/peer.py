from Models.Peer import Peer
import threading
import os
import time
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

def request_chunk(file, port_no, chunk_no):
    peer.request_chunk(file, port_no, chunk_no)

def ask_peers(file):
    print("Request for file : ", file)
    peer.file_chunk = []
    peer.file_size = 0
    peer.received_file = {}
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
    print("File chunks : ",peer.file_size)

    time.sleep(3)

    chunks_wanted = [i for i in range(peer.file_size)]
    while len(chunks_wanted):
        index = 0
        peer_found = False
        threads = []
        for chunk in chunks_wanted:
            while len(peer.peer_list) and (index < len(peer.file_chunk)) and (peer.file_chunk[index] not in peer.peer_list):
                index += 1
            if index < len(peer.file_chunk):
                peer_found = True
                t = threading.Thread(target=request_chunk, args=(file, peer.file_chunk[index], chunk))
                t.start()
                threads.append(t)
                
            index = (index + 1)%len(peer.file_chunk)
        
        if not peer_found:
            print("No peers found for file : ", file)
            return

        for t in threads:
            t.join()
        
        for chunk in peer.received_file:
            if chunk in chunks_wanted:
                chunks_wanted.remove(chunk)
    if len(peer.received_file):
        peer.add_file_to_folder(file)

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
    
    if action.split(" ")[0].lower() == "need":
        file = action.split(" ")[1]
        if not peer.check_if_file_exist(file):
            t = threading.Thread(target=ask_peers, args=(file,))
            t.start()
        else:
            print("File already exists")