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
        self.down = Down()

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

    def is_lowered(self):
        return len(self.down)>0

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
        fmt = '[{:2}]'
        if code=='MSG':
            print msg_spl[1]
        elif code=='NONE':
            pass
        elif code=='HAND':
            hand = json.loads(msg_spl[1])
            self.hand = Hand(*hand)
            print 'Your hand:'
            print hand
            print '  '.join([fmt.format(i+1) for i in range(len(hand))])
        elif code=='DISCARD':
            discard = json.loads(msg_spl[1])
            self.discard = Card(*discard)
            print 'Discard:'
            print discard
        elif code=='CARD':
            card = json.loads(msg_spl[1])
            self.hand.append(Card(*card))
            print 'Your new card:'
            print self.hand[-1]
            print fmt.format(len(self.hand))
        elif code=='TURN':
            self.play(msg_spl[1])
            # Check
            assert len(self.hand)<=12

    def play(self, game):
        # Draw a card
        ans = interact('Pick up a card from [t]op of the deck or [d]iscard? ',
            't', 'd')
        if ans=='d':
            action = 0
            self.hand.append(self.discard)
            print 'Discard card is [{:2}]'.format(len(self.hand))
        else:
            action = 1
        self.send('DRAW|%i' % action)
        msg = self.receive()
        self.decode(msg)
        
        # Lower hand or drop
        if self.is_lowered:
            # Discard or drop cards to lowered cards
            ans = interact('Would you like to [d]iscard a card or [l]ower cards? ', 
                    'd', 'l')
            if ans=='l':
                self.lower_cards()
        else:
            ans = interact('Would you like to [d]iscard a card or [l]ower your hand? ',
                    'd', 'l')
            if ans=='l':
                # Ask for cards to lower
                self.lower_hand(game)

        # Always discard a card at the end
        ans = interact('What card would you like to discard [1-%i]? ' % \
                len(self.hand), *range(1, len(self.hand)+1))
        ans = int(ans)-1
        self.discard = self.hand.pop(ans)
        self.send('DISCARD|%i' % ans)

        print 'Your turn has ended'

    def lower_hand(self, game):
        
        # Determine number of three-of-a-kind or straights in the round
        if 'T' in game and 'S' in game:
            nt = int(game[0])
            ns = int(game[2])
        elif 'T' in game:
            nt = int(game[0])
            ns = 0
        else:
            nt = 0
            ns = int(game[0])

        self.lower_cards(nt, 'three-of-a-kind')
        self.lower_cards(ns, 'straights')

    def lower_cards(self, n, msg):
        text = 'Lower a %s (coma separated): ' % msg
        for i in range(n):
            lowered = False
            while not lowered:
                cards = interact_size(text, 3)
                lowered = self.lower(cards)

    def lower(self, cards, to_lower=None):
        msg = json.dumps(cards)
        self.send('LOWER|'+msg)
        flag = self.receive()
        if flag is '1':
            return True
        else:
            return False




