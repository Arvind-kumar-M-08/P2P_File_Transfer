from Models.Manager import Manager
import threading
import subprocess
from time import sleep


manager = Manager(10000)

def new_peer(c, port_no):
    manager.add_peer(c, port_no)
    
def listen_for_message():
    while True:
        c, addr = manager.s.accept() 
        print("Conncetion from ", addr[1])
        message = c.recv(1024).decode()
        if message == "HI":
            print("New connection request")
            t = threading.Thread(target=new_peer, args=(c, addr[1], ))
            t.start()


try:
    listen_for_message()
except Exception as e:
    manager.s.close()

finally:
    manager.s.close()