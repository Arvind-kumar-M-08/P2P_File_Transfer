from Models.Manager import Manager
import threading

manager = Manager(10000)

def listen_for_message():
    while True:
        c, addr = manager.s.accept() 
        print("Conncetion from ", addr)
        c.send("Hi".encode())
        c.close()


listen_for_message()