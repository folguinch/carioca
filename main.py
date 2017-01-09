from .utils import greeting, ROUNDS
from .player import client
from .dealer import Dealer

def main_server():

    # Greeting message
    greeting()

    # Initialise users
    # This should only be done by the server and sent to the clients
    players = Dealer()
    
    for i,(key,val) in enumerate(ROUNDS.items()):
        # Current round
        print "Round: %i" % (i+1)
        print "Objective: %s" % val

        # Create the deck
        print "Creating and shuffling card deck"
        players.get_deck(game=key)

        # Draw cards
        players.draw()
        break


        #### TO DO ####
        # Cutting the deck


def main():
    greeting()
    player_name = raw_input('Player name:')
    nplayers = raw_input('Number of players:')

    # Connect to server
    import socket

    # Connect the socket to the port where the server is listening
    server_address = ('ganymede', 10000)
    sock.connect(server_address)
    sock.sendall('%s,%s' % (nplayers, player_name))
