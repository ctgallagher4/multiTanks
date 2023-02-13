import pickle
import socket
import time
from threading import Thread, Lock
import sys

class Server:

    def __init__(self):
        self.ip = ""
        self.port = 5555
        self.recvSock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDPsock.bind((UDP_IP, UDP_PORT))
        self.recvSock.bind((self.ip, self.port))
        self.sendSock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDPsock.bind((UDP_IP, UDP_PORT))
        self.addrs = []
        self.lock = Lock()
        self.data = None

    def listenThread(self):
        while True:
            data, addr = self.recvSock.recvfrom(1024)
            with self.lock:
                if addr not in self.addrs:
                    self.addrs.append(addr)
                self.data = data
            time.sleep(1/1000)

    def broadcastThread(self):
        while True:
            with self.lock:
                addrs = self.addrs.copy()
                data = self.data
            for addr in addrs:
                self.recvSock.sendto(data, addr)
            length = len(addrs)
            sizeof = sys.getsizeof(self.data)
            print(f"sent: {sizeof}, to {length}")
            time.sleep(1/10)

    def run(self):
        Thread(target = self.listenThread).start()
        Thread(target = self.broadcastThread).start()

serv = Server()
serv.run()
