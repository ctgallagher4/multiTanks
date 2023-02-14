import pickle
import socket
import time

class Server:

    def __init__(self):
        self.ip = ""
        self.port = 5555
        self.recvSock = socket.socket(socket.AF_INET,
                                      socket.SOCK_DGRAM)
        self.recvSock.bind((self.ip, self.port))
        self.sendSock = socket.socket(socket.AF_INET, # Internet
                                      socket.SOCK_DGRAM)
        self.addrs = []
        self.data = None
        self.player1Loaded = False
        self.player2Loaded = False

    def transcieve(self):
        while True:
            data, recvAddr = self.recvSock.recvfrom(1024)
            message = dict(pickle.loads(data))
            if 'player1' in message.keys():
                self.player1 = recvAddr
                self.player1Loaded = True
                if self.player2Loaded:
                    self.recvSock.sendto(data, self.player2)
                    print("sent", message)
            elif 'player2' in message.keys():
                self.player2 = recvAddr
                self.player2Loaded = True
                if self.player1Loaded:
                    self.recvSock.sendto(data, self.player1)
                    print("sent", message)

            time.sleep(1/100)

    def run(self):
        self.transcieve()

serv = Server()
serv.run()
