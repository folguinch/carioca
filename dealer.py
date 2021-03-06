from ConfigParser import ConfigParser
from operator import attrgetter

from .player import Client
from .cards import *
from .utils import init_server
from .decoder import decode_msg

class Dealer(list):

    def __init__(self):

        # Initialise server
        self.sock = init_server()
        players = self.connect_players()

        self.deck = None
        self.discard = None
        self.table = None

    def __str__(self):
        table = sorted(self, key=attrgetter('points','name'), reverse=True)
        fmt = '[%i] %s\t\t%i\n'
        line = ''
        for i,p in enumerate(table):
            line += fmt % (i+1, p.name, p.points)
        return line.strip()

    @property
    def names(self):
        return [p.name for p in self]

    def index(self, player):
        for i, p in enumerate(self):
            if p.name == player.name:
                return i

    def get_players(self, filename):
        """
        Initialize players from a configuration file.
        """
        config = ConfigParser()
        read = config.read(filename)
        print 'Players:'
        for name in config.sections():
            print '\t%s' % name
            self.append(Client(name, config.get(name,'ip')))

    def connect_players(self, msg_length=2048):

        # Get player names and addresses
        # Each player must enter the total number of players but the last one
        # to connect will determine how many will participate
        while True:
            # Wait for a connection
            print 'Waiting for players'
            connection, client_address = self.sock.accept()
            data = ''

            try:
                print 'Connection from', client_address
                while True:
                    msg = connection.recv(msg_length)
                    data += msg
                    if len(data)==0:
                        continue
                    if len(msg)<msg_length:
                        connection.sendall('1')
                        break
            except:
                continue

            nplayers, name = data.split(',')
            nplayers = int(nplayers)
            if len(self)== 0:
                print 'Number of players:', nplayers
            self.sendall('MSG|%s has connected' % name)
            self.append(Client(name, connection))

            if len(self)==nplayers:
                break

    def sendall(self, msg):
        for player in self:
            player.send(msg)

    def send_exclude(self, exclude, msg):
        for player in self:
            if player.name!=exclude.name:
                player.send(msg)

    def get_deck(self, game):
        self.deck = Deck(game=game)
        self.discard = Discard()

    def update_points(self):
        for player in self:
            player.send('POINTS')
            msg = player.receive()
            code, points = msg.split('|')
            player.points += int(points)
        
        self.sendall('MSG|%s' % self)


    def reset_table(self, names):
        self.table = Table(names)

    def draw(self):
        """
        Draw 12 cards to each player and leave one in the discard.
        """
        nplayers = len(self)
        print 'Drawing cards'
        hands = []
        for i in range(nplayers*12):
            card = self.deck.pop()
            try:
                hands[i % nplayers].append(card)
            except IndexError:
                hands.append(Hand())
                hands[i % nplayers].append(card)

        # Leave one card in the discard
        self.discard.append(self.deck.pop())

        # Send hand to each player
        for i,player in enumerate(self):
            player.send('HAND|'+hands[i].encode())
            player.send('DISCARD|'+self.discard[-1].encode())

    def decode(self, msg, player):
        if len(msg)==0:
            return True

        code, action = msg.split('|')
        i = self.index(player)
        if code=='DRAW':
            action = int(action)
            if action==1:
                card = self.deck.pop()
                #self[i].hand.append(card)
                player.send('CARD|'+card.encode())
            elif action==0:
                card = self.discard[-1]
                self.discard = self.discard[:-1]
                #self[i].hand.append(card)
                player.send('NONE|0')
                newmsg = 'MSG|Player %s picked-up the discard card'
                self.send_exclude(player, newmsg % player.name)
            return True
        #elif code=='LOWER':
        #    self[i].lower(action)
        elif code=='TABLE':
            was_lowered = self.table[player.name] is not None
            self.table = decode_msg(action)
            self.send_exclude(player, 'TABLE|'+self.table.encode())
            is_lowered = self.table[player.name] is not None
            if was_lowered != is_lowered:
                newmsg = 'MSG|Player %s has lowered' % player.name
                self.send_exclude(player, newmsg)
            return True
        elif code=='DISCARD':
            print action
            self.discard.append(decode_msg(action))
            self.send_exclude(player, 'DISCARD|'+self.discard[-1].encode())
            return True
        elif code=='WIN':
            newmsg = 'MSG|Player %s has won' % player.name
            self.sendall(newmsg)
            # Get the points
            self.update_points()
            return -1
        elif code=='FINISH':
            return False




