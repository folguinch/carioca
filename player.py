import socket, json

from .cards import Hand, Down
from .base import Card
from .utils import interact

__metaclass__ = type

class BasePlayer:

    def __init__(self, name):
        self.name = name
        self.socket = None
        self.reset()

    def reset(self):
        self.hand = Hand()
        self.Down = Down()

    def send(self, msg):
        assert self.socket is not None

        # Send message
        self.socket.sendall(msg)

        # Wait for reply
        answer = self.socket.recv(1)

        if answer!='1':
            raise Exception('Connection error')

    def receive(self, msg_length=2048):
        assert self.socket is not None
        data = ''
        while True:
            msg = self.socket.recv(msg_length)
            data += msg
            if len(data)==0:
                continue
            elif len(msg)<msg_length:
                self.socket.sendall('1')
                break
        return data

class Player(BasePlayer):

    def __init__(self, name, socket):
        print 'New player:', name 
        super(Player, self).__init__(name)
        self.socket = socket

class Client(BasePlayer):

    def __init__(self, name):
        # Create a TCP/IP socket
        super(Client, self).__init__(name)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.discard = None

    def connect(self, host, port):
        print 'Connecting to %s port %s' % (host, port) 
        self.socket.connect((host, port))

    def decode(self, msg):
        msg_spl = msg.split('|')
        code = msg_spl[0]
        if code=='MSG':
            print msg_spl[1]
        elif code=='HAND':
            hand = json.loads(msg_spl[1])
            self.hand = Hand(*hand)
            print 'Your hand:'
            print self.hand
        elif code=='DISCARD':
            discard = json.loads(msg_spl[1])
            self.discard = Card(*discard)
            print 'Discard:'
            print self.discard
        elif code=='CARD':
            card = json.loads(msg_spl[1])
            self.hand.append(Card(*card))
            print 'Your new card:'
            print self.hand[-1]
        elif code=='TURN':
            self.play()

    def play(self):
        ans = interact('Pick up a card from [t]op of the deck or [d]iscard?',
            't', 'd')

        if ans=='d':
            self.hand.append(self.discard)
        else:
            self.send('DRAW|1')
            msg = self.receive()
            self.decode(msg)
        

