import socket
import pygame
import pickle
from Utilities.Constants import *
from Utilities.__init__ import *
from Objects.Tank import Tank
import sys

class Transciever:

    def __init__(self, name, ipSend, portSend):
        self.name = name
        self.sendSock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM)
        self.portSend = portSend
        self.ipSend = ipSend
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('shadowTanks')
        self.clock = pygame.time.Clock()
        self.fontEnd = pygame.font.SysFont('timesnewroman', 300)
        self.fontLife = pygame.font.SysFont('timesnewroman', 100)
        self.fontDuring = pygame.font.SysFont('timesnewroman', 100)
        self.fontfps = pygame.font.SysFont('timesnewroman', 50)
        self.score = 0
        self.objects = []
        self.bulletThresh = 0
        self.bullets = []
        self.fuel = 100
        self.health = 100
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
        self.gameOn = True

    def eventListener(self):
        '''A method to listen for events, specifically quit'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.gameOn = False

    def setup(self):
        self.player1 = Tank(self, self.surface, "assets/tank_body.png", 
                        "assets/turret.png", WIDTH/2, HEIGHT/2, lightOn = False)
        self.player2 = Tank(self, self.surface, "assets/tank_body_red.png", 
                        "assets/turret_red.png", WIDTH/2, HEIGHT/2, lightOn = False)

    def pause(self):
        '''A method to pause the game'''
        pygame.time.wait(500)
        while self.eventListener():
            self.displayScore()
            pause = self.fontLife.render("Press spacebar to continue...", 
                                            False, WHITE, BLACK)
            self.surface.blit(pause, (WIDTH/5, HEIGHT/3))
            pygame.display.flip()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] == 1:
                self.reset()
                break

    def display(self):
        self.surface.fill(WHITE)

    def tickFlip(self):
        self.clock.tick(FRAME_RATE)
        pygame.display.update()

    def update(self):
        self.player1.update()
        self.player2.update()
        msg = pickle.dumps({self.name: {"x": round(self.player1.x, 3), 
                                    "y": round(self.player1.y, 3),
                                    "dir": round(self.player1.dir, 3),
                                    "turDir": round(self.player1.turDir, 0)}})
        self.sendSock.sendto(msg, (self.ipSend, self.portSend))

    def recvServerUpdate(self):
        data, addr = self.sendSock.recvfrom(1024)
        message = dict(pickle.loads(data))
        if self.name == "player1" and ("player2" in message.keys()):
            self.player2.x = message["player2"]["x"]
            self.player2.y = message["player2"]["y"]
            self.player2.dir = message["player2"]["dir"]
            self.player2.turDir = message["player2"]["turDir"]
        if self.name == "player2" and ("player1" in message.keys()):
            self.player2.x = message["player1"]["x"]
            self.player2.y = message["player1"]["y"]
            self.player2.dir = message["player1"]["dir"]
            self.player2.turDir = message["player1"]["turDir"]

    def run(self):
        self.setup()
        while self.gameOn:
            self.display()
            self.update()
            self.recvServerUpdate()
            self.tickFlip()
            self.eventListener()
        
        self.sendSock.close()

if __name__ == '__main__':
    name = input("player1/player2: ")
    address = input("local/remote: ")
    if address == "local":
        goTo = "127.0.0.1"
    if address == "remote":
        goTo = "143.42.128.64"
    trans = Transciever(name, goTo, 5555)
    trans.run()