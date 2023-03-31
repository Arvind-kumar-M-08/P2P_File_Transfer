from Models.Manager import Manager
import threading
import subprocess
from time import sleep


manager = Manager(10000)
lock = threading.Lock()
def update_peer_list():
    with lock:
        
def new_peer(c, port_no):
    manager.add_peer(c, port_no)
    t = threading.Thread(target=listen_to_peer, args=(c, port_no))
    t.start()

def remove_peer(port_no):
    manager.remove_peer(port_no)

def listen_to_peer(conn, port_no):
    while True:
        message = conn.recv(1024).decode()

        if message == "BYE":
            print("Peer leaving at port : ", port_no)
            t = threading.Thread(target=remove_peer, args=(port_no,))
            t.start()
    
def listen_for_connection():
    while True:
        c, addr = manager.s.accept() 
        print("Conncetion from ", addr[1])
        
        #New peer
        print("New connection request from port : ",addr[1])
        t = threading.Thread(target=new_peer, args=(c, addr[1], ))
        t.start()            

def check_active_peers():
    while True:
        sleep(5)
        print("Checking active peers")
        manager.check_peer()

try:
    t = threading.Thread(target=check_active_peers)
    t.start()
    listen_for_connection()

except KeyboardInterrupt:
    manager.s.close()
