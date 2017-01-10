import socket, json

from .cards import Hand, Down
from .base import Card

__metaclass__ = type

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


class Client(BasePlayer):

    def __init__(self, name):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        super(Client, self).__init__(name)
        self.discard = None

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

    def decode(self, msg):
        msg_spl = msg.split('|')
        code = msg_spl[0]
        if code == 'HAND':
            hand = json.loads(msg_spl[1])
            self.hand = Hand(*hand)
            print 'Your hand:'
            print self.hand
        elif code == 'DISCARD':
            discard = json.loads(msg_spl[1])
            self.discard = Card(*discard)
            print 'Discard:'
            print discard

