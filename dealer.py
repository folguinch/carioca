from ConfigParser import ConfigParser

from .cards import *
from .utils import init_server

class Dealer(list):

    def __init__(self):

        # Initialise server
        self.sock = init_server()
        players = self.connect_players()

        self.deck = None
        self.discard = None

    def get_players(self, filename):
        """
        Initialize players from a configuration file.
        """
        config = ConfigParser()
        read = config.read(filename)
        print 'Players:'
        for name in config.sections():
            print '\t%s' % name
            self.append(Player(name, config.get(name,'ip')))

    def connect_players(self):

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
                    msg = connection.recv(16)
                    if msg:
                        data += msg
                    else:
                        break
            except:
                continue

            nplayers, name = data.split(',')
            nplayers = int(nplayers)
            if len(self)== 0:
                print 'Number of players:', nplayers
            self.append(Player(name, connection))

            if len(self)==nplayers:
                break

    def get_deck(self, game):
        self.deck = Deck(game=game)
        self.discard = Discard()

    def draw(self):
        """
        Draw 12 cards to each player and leave one in the discard.
        """
        nplayers = self.__length__()
        print 'Drawing cards'
        for i in range(nplayers*12):
            card = self.deck.pop()
            self.players[i % nplayers].hand.append(card)

        # Leave one card in the discard
        self.discard.append(self.deck.pop())



