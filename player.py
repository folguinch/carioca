from ConfigParser import ConfigParser

from .cards import *
from .utils import get_players

class Player:

    def __init__(self, name, ip):
        self.name = name
        self.ip = ip
        self.hand = None
        self.down = None

class Players(list):

    def __init__(self, players):
        players = get_players(players)
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

    def get_deck(self, game):
        self.deck = Deck(game=game)
        self.discard = Discard()
