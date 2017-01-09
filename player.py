import socket

from .cards import Hand, Down

class BasePlayer:

    def __init__(self, name):
        self.name = name
        self.reset()

    def reset(self):
        self.hand = Hand()
        self.Down = Down()

class Player(BasePlayer):

    def __init__(self, name, socket):
        print 'New player:', name 
        self.socket = socket
        super(Player, self).__init__(name)


class Client:

    def __init__(self, name):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        super(Player, self).__init__(name)

    def connect(self, host, port):
        print 'Connecting to %s port %s' % (host, port) 
        self.sock.connect((host, port))

    def send(self, msg):
        self.sock.sendall(msg)

    def receive(self, msg_length=2048):
        data = ''
        while True:
            msg = self.sock.recv(msg_length)
            data += msg
            if len(msg)<msg_length:
                break
        return data

