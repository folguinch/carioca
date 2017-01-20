import socket

from .cards import Hand, Down, Table
from .decoder import decode_msg
from .utils import interact, get_values_seq

__metaclass__ = type

class BasePlayer:

    def __init__(self, name):
        self.name = name
        self.socket = None
        self.points = 0
    #    self.reset()

    #def reset(self):
    #    self.hand = Hand()
    #    self.table = None

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

    #def lower(self, cards):
    #    if len(cards)==3:
    #        down = self.hand.lower_three(cards)
    #    elif len(cards)==4:
    #        down = self.hand.lower_straight(cards)

class Client(BasePlayer):

    def __init__(self, name, socket):
        print 'New player:', name 
        super(Player, self).__init__(name)
        self.socket = socket

    #def is_lowered(self):
    #    return len(self.down)>0

class Player(BasePlayer):

    def __init__(self, name):
        # Create a TCP/IP socket
        super(Client, self).__init__(name)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.discard = None
        self.reset()

    def reset(self):
        self.hand = Hand()
        self.table = None

    def connect(self, host, port):
        print 'Connecting to %s port %s' % (host, port) 
        self.socket.connect((host, port))

    def print_current(self):
        self.print_hand()
        self.print_discard()
        self.print_table()

    def print_hand(self):
        print 'Your hand:'
        print self.hand

    def print_discard(self):
        print 'Discard:'
        print self.discard
    
    def print_table(self):
        if self.table.is_empty():
            print 'None has lowered'
        else:
            print 'Lowered:'
            print self.table

    def encode(self):
        return self.hand.encode() + '|'+ self.table.encode()

    def decode(self, msg):
        msg_spl = msg.split('|')
        code = msg_spl[0]
        fmt = '[{:2}]'
        if code=='MSG':
            print msg_spl[1]
        elif code=='NONE':
            pass
        elif code=='HAND':
            self.hand = decode_msg(msg_spl[1])
            self.print_hand()
        elif code=='DISCARD':
            self.discard = decode_msg(msg_spl[1])
            self.print_discard()
        elif code=='CARD':
            self.hand.append(decode_msg(msg_spl[1]))
            print 'Your new card:'
            print self.hand[-1]
            print fmt.format(len(self.hand))
        elif code=='TABLE':
            self.table = decode_msg(msg_spl[1])
        elif code=='POINTS':
            points = self.hand.get_points()
            self.points += points
            self.send('POINTS|%i' % points)
        elif code=='TURN':
            print '-'*80 
            print "It's your turn!"
            self.play(msg_spl[1])
            # Check
            assert len(self.hand)<=12
            print 'Your turn has ended'
            print '-'*80 

    def is_lowered(self):
        return self.table[self.name] is not None

    def play(self, game):
        # Print current status
        self.print_current()

        # Draw a card
        ans = interact('Pick up a card from [t]op of the deck or [d]iscard? ',
            't', 'd')
        if ans=='d':
            action = 0
            self.hand.append(self.discard)
            print 'Discard card is [{:2}]'.format(len(self.hand))
        else:
            action = 1
        # Inform server about the action and decode the server message
        self.send('DRAW|%i' % action)
        msg = self.receive()
        self.decode(msg)
        
        # Lower hand or drop
        win = False
        if self.is_lowered():
            # Discard or drop cards to lowered cards
            msg = 'Would you like to [d]iscard a card or [l]ower cards? '
            ans = interact(msg, 'd', 'l')
            if ans=='l':
                win = self.drop_cards()
                print 'Your cards have been lowered'
        else:
            msg = 'Would you like to [d]iscard a card or [l]ower your hand? '
            ans = interact(msg, 'd', 'l')
            if ans=='l':
                # Ask for cards to lower
                win = self.lower_hand(game)
                print 'Your cards have been lowered'

        # Inform the status to the server
        self.send('TABLE|%s' % self.table.encode())

        # Always discard a card at the end
        if not win:
            ans = interact('What card would you like to discard [1-%i]? ' % \
                    len(self.hand), *range(1, len(self.hand)+1))
            ans = int(ans)-1
            self.discard = self.hand.pop(ans)
            self.send('DISCARD|%i' % ans)
        else:
            self.send('WIN|1')

    def lower_hand(self, game):
        # Copy of the current hand in pickle format
        hand = self.hand.encode()

        # Iterate over game
        for g in range(0, len(game), 2):
            try:
                n = int(g[0])
                t = g[1]
                lowered = self._lower_hand(n, t)
                # If fail restore hand and continue game
                if not lowered:
                    self.hand = decode_msg(hand)
                    self.table.reset(self.name)
                    break

            except ValueError:
                assert game=='RS'
                lowered = self.lower_rs()
                # The player wins
                return True
        # The player has not won
        return False

    def _lower_hand(self, n, game):
        msg = 'three-of-a-kind' if game=='T' else 'straight'
        text = 'Lower a %s or [c]ancel (coma separated): ' % msg
        for i in range(n):
            lowered = False
            while not lowered:
                cards = interact_size(text, 'c', size=size, dtype=int,
                        delimeter=',')
                if cards=='c':
                    return False
                lowered = self.lower(cards)
            print '%i/%i %s lowered' % (i+1, n, msg)

        return True

    def lower_rs(self):
        print 'Trying to lower a Real straight'
        self.hand.sort()
        seq = get_values_seq()
        for i, card in enumerate(self.hand):
            if str(card.value)[0] == seq[i]:
                continue
            else:
                print 'Not a Real straight'
                print 'Your hand:'
                print self.hand

        return True

    def drop_cards(self):
        for i, player in enumerate(self.table):
            msg = 'Which cards would you lower on [%i] %s (coma separated): '
            ans = interact(msg % (i+1, player), '', dtype=int, delimeter=',')
            if ans=='':
                continue
            else:
                for card in ans:
                    flag = self.table.insert_card(player, self.hand[card])
                    if flag:
                        self.hand[card] = None
                    else:
                        print 'Card %i cannot be lowered' % card
                    # If the player won do not continue dropping cards
                    if len(self.hand)==1:
                        return True

        self.hand.compact()
        if len(self.hand)==1:
            return True
        else:
            return False

    def lower(self, cards):
        if len(cards)==3:
            down = self.hand.lower_three(cards)
        elif len(cards)==4:
            down = self.hand.lower_straight(cards)

    #def lower(self, cards, to_lower=None):
    #    msg = json.dumps(cards)
    #    self.send('LOWER|'+msg)
    #    flag = self.receive()
    #    if flag is '1':
    #        return True
    #    else:
    #        return False




