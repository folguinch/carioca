import json
from itertools import cycle

from .utils import greeting, ROUNDS
from .player import Player
from .dealer import Dealer

def main_server():

    # Greeting message
    greeting()

    # Initialise users
    # This should only be done by the server and sent to the clients
    players = Dealer()
    
    for i,(key,val) in enumerate(ROUNDS.items()):
        # Current round
        msg = "Round: %i\nObjective: %s" % (i+1, val)
        print msg
        players.sendall('MSG|'+msg)

        # Inform the players about the turns
        msg = 'Playing order:\n'
        msg += '\n'.join(players.names)
        players.sendall('MSG|'+msg)

        # Initialize the table
        players.reset_table(players.names)
        players.sendall('TABLE|'+players.table.encode())

        # Create the deck
        print "Creating and shuffling card deck"
        players.get_deck(game=key)

        # Draw cards
        players.draw()

        # Play
        for player in cycle(players):
            # Inform the player it is its turn
            player.send('TURN|%s' % key)

            # Inform the other players to wait
            msg = 'Waiting for %s to play' % player.name
            players.send_exclude(player, 'MSG|'+msg)
            print msg

            # Wait for the player to answer
            while True:
                msg = player.receive()
                flag = players.decode(msg, player)
                if flag==-1:
                    break
                elif flag:
                    continue
                elif not flag:
                    break
                else:
                    raise ValueError('Flag not recognised')

            if flag==-1:
                break

        # Rotate players
        break


        #### TO DO ####
        # Cutting the deck


def main():
    greeting()
    player_name = raw_input('Player name:')
    nplayers = raw_input('Number of players:')

    # Connect to server
    player = Player(player_name)

    # Connect the socket to the port where the server is listening
    player.connect('ganymede', 10000)
    player.send('%s,%s' % (nplayers, player_name))

    while True:
        msg = player.receive()
        if len(msg)>0:
            player.decode(msg)
