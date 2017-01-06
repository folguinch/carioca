from .utils import greeting, ROUNDS

def main(args):

    # Greeting message
    greeting()

    # Initialise users
    # This should only be done by the server and sent to the clients
    players = Players(args.players)
    
    for i,(key,val) in enumerate(ROUNDS.items()):
        # Current round
        print "Round: %i" % (i+1)
        print "Objective: %s" % val

        # Create the deck
        print "Creating and shuffling card deck"
        players.get_deck(game=key)

        # Draw cards
        players.draw()


        #### TO DO ####
        # Cutting the deck
