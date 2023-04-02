"""Module providingFunction for manager in peer-peer application"""
import os
import threading
from time import time
from Models.Manager import Manager

manager = Manager(10000)

# Lock for updating peer list
lock = threading.Lock()


def update_peer_list(msg, peer):
    """
    Updates the active peer list in manager

    Args:
        msg (str): addtion or deletion
    """
    with lock:
        if msg == "add":
            manager.peer_list.append(peer)
        elif msg == "del":
            manager.peer_list.remove(peer)

def new_peer(c, addr, ppport):
    update_peer_list("add", (c, addr, ppport))
    manager.send_peerlist()

    #Listening to connected peer
    t = threading.Thread(target=listen_to_peer, args=(c, addr))
    t.start()

def remove_peer(addr):
    for peer in manager.peer_list:
        if peer[1] == addr:
            update_peer_list("del", peer)
            break
    manager.send_peerlist()

#checking if peer is active
def listen_to_peer(conn, addr):
    last_sent_time = time()
    is_alive_check = False
    while True:

        if time() - last_sent_time > 10 :
            is_alive_check = True
            last_sent_time = time()
            print("Cheking alive for peer at : ", addr)
            try:
                conn.send("ALIVE_CHECK".encode())
            except BrokenPipeError:
                print("Peer dead at : ", addr)
                t = threading.Thread(target=remove_peer, args=(addr,))
                t.start()
                t.join()
                # manager.send_peerlist()
                return
        try:
            conn.settimeout(5)
            message = conn.recv(1024).decode()

            if message == "BYE":
                print("Peer leaving at port : ", addr)
                t = threading.Thread(target=remove_peer, args=(addr,))
                t.start()
                t.join()
                return

            if message == "OK":
                is_alive_check = False
                continue
        except:
            if is_alive_check:
                print("Peer dead at : ", addr)
                t = threading.Thread(target=remove_peer, args=(addr,))
                t.start()
                t.join()
                return
        finally:
            is_alive_check = False


def listen_for_connection():
    while True:
        c, addr = manager.s.accept() 
        try:
            # Message is "Hi PeerPort"
            message = int(c.recv(1024).decode().split()[1])
            print("Peer - peer port: ", message)
            print("New connection request from : ",addr)
            t = threading.Thread(target=new_peer, args=(c, addr, message,))
            t.start()    
        except:
            print("Error while adding new peer")


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
    action = input()
    if action.lower() == "close" or action.lower() == "c":
        print("Closing Manager")
        os._exit(0)
