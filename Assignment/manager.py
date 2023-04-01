from Models.Manager import Manager
import threading
import subprocess
from time import sleep, time
import os

manager = Manager(10000)

# Lock for updating peer list
lock = threading.Lock()

def update_peer_list(msg, peer):
    print(msg, " peer list atomically")
    with lock:
        if msg == "add":
            manager.peer_list.append(peer)
        elif msg == "del":
            manager.peer_list.remove(peer)

def new_peer(c, port_no, ppport):
    # manager.add_peer(c, port_no)
    update_peer_list("add", (c, port_no, ppport))
    manager.send_peerlist()

    #Listening to connected peer
    t = threading.Thread(target=listen_to_peer, args=(c, port_no))
    t.start()

def remove_peer(port_no):
    for peer in manager.peer_list:
        if peer[1] == port_no:
            update_peer_list("del", peer)
            break
    manager.send_peerlist()

#checking if peer is active
def listen_to_peer(conn, port_no):
    last_sent_time = time()
    is_alive_check = False
    while True:
        temp = [peer[1] for peer in manager.peer_list]
        print(temp)
        print("Number of peers ", len(manager.peer_list))
        if time() - last_sent_time > 10 :
            is_alive_check = True
            last_sent_time = time()
            print("Cheking alive for peer at : ", port_no)
            try:
                conn.send("ALIVE_CHECK".encode())
            except BrokenPipeError:
                print("Peer dead at : ", port_no)
                t = threading.Thread(target=remove_peer, args=(port_no,))
                t.start()
                t.join()
                # manager.send_peerlist()
                return
        try:
            conn.settimeout(5)
            message = conn.recv(1024).decode()

            if message == "BYE":
                print("Peer leaving at port : ", port_no)
                t = threading.Thread(target=remove_peer, args=(port_no,))
                t.start()
                t.join()
                return

            if message == "OK":
                is_alive_check = False
                continue
        except:
            print("is check alive ", is_alive_check)
            if is_alive_check:
                print("Peer dead at : ", port_no)
                t = threading.Thread(target=remove_peer, args=(port_no,))
                t.start()
                t.join()
                return
        finally:
            is_alive_check = False


def listen_for_connection():
    while True:
        c, addr = manager.s.accept() 
        print("Conncetion from ", addr[1])
        try:
            message = int(c.recv(1024).decode().split()[1])
            print("Peer - peer port: ", message)
            #New peer
            print("New connection request from port : ",addr[1])
            t = threading.Thread(target=new_peer, args=(c, addr[1], message,))
            t.start()    
        except:
            print("Error while adding peer")


def is_active_peers_changed():
    last_checked_time = time()
    old = [peer[1] for peer in manager.peer_list]
    while True:
        if time() - last_checked_time > 5:
            print("Checking if peers changed")
            new  = [peer[1] for peer in manager.peer_list]

            if not sorted(old) == sorted(new):
                print("Peers changed : Broadcasting")
                manager.send_peerlist()
                old = new
            last_checked_time = time()


t1 = threading.Thread(target=is_active_peers_changed)
t1.start()
t2 = threading.Thread(target=listen_for_connection)
t2.start()

while True:
    action = input("INPUT : ")
    if action.lower() == "close" or action.lower() == "c":
        print("Closing Manager")
        os._exit(0)

