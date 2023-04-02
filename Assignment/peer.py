"""Module providingFunction for peer in peer-peer application"""
import os
import threading
from Models.Peer import Peer

port_no = int(input("Enter port number : "))
name = input("Peer number : ")

peer = Peer(port_no, "peer" + name + "/")

peer.join()

stop_flag = threading.Event()

def update_peer():
    while not stop_flag.is_set():
        peer.update_peer();

def listen_to_peers():
    peer.listen_to_peers()

def ask_a_peer(file, otherPeer):
    peer.ask_a_peer(file, otherPeer)

def request_chunk(file, other_peer, chunk_no):
    peer.request_chunk(file, other_peer, chunk_no)

def ask_peers(file):
    peer.file_chunk = []
    peer.file_size = 0
    peer.received_file = {}
    threads = []
    for p in peer.peer_list:
        if p[1] != peer.port or p[0] != peer.ip:
            t = threading.Thread(target=ask_a_peer, args=(file, p,))
            t.start()
            threads.append(t)
    
    # waiting till all threads append chunk info
    for t in threads:
        t.join()

    print("------FILE CHUNKS------")
    print("Number of chunks : ",peer.file_size)
    print("Peers having the file ", file)
    print(peer.file_chunk)
    
    chunks_wanted = list(range(peer.file_size))
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
    action = int(input("Enter a action (0, 1, 2, 3) : "))
    print("\n")
    if action == 0:
        file = input("Enter a file name : ")
        print("\n")
        if not peer.check_if_file_exist(file):
            t = threading.Thread(target=ask_peers, args=(file,))
            t.start()
            t.join()
        else:
            print("File already exists")
    
    elif action == 1:
        print("List of shareable files")
        for file in peer.shareable_files:
            print(file, sep="\t")

    elif action == 2:
        print("List of active peers")
        print("\tIP\t\t\tPort")
        for p in peer.peer_list:
            print("\t",p[0],"\t\t",p[1])
    
    elif action == 3:
        print("Closing peer")
        stop_flag.set()
        peer.leave()
        os._exit(0)

    else:
        print("Enter a valid action (0, 1, 2, 3)")

    print("\n")
