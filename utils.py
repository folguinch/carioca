import socket
from itertools import product, repeat, chain
from collections import OrderedDict

SUITS_UNICODE = {'spades':u'[%s\u2660]', 'hearts':u'[%s\u2665]',
        'diamonds':u'[%s\u2666]', 'clubs':u'[%s\u2663]',
        'red_joker':u'[ \u2606]', 'black_joker':u'[ \u2605]'}

VALUES = OrderedDict(zip(range(2,11)+['J','Q','K','A','W'], 
    range(2,11)+[10,10,10,15,30]))

ROUNDS = {'2T':'2 three-of-a-kind', '1T1S':'1 three-of-a-kind & 1 straight',
        '2S':'2 straights', '3T':'3 three-of-a-kind', 
        '2T1S':'2 three-of-a-kind & 1 straight', 
        '1T2S':'1 three-of-a-kind & 2 straights', 'RS':'Real straight'}

def validate_card(value, suit):
    assert suit in SUITS_UNICODE.keys()
    assert value in VALUES.keys()

    if value=='W' and suit not in ['red_joker','black_joker']:
        raise ValueError('Card value does not match a valid suit')

def get_deck(ndecks=1, include_joker=True):
    suits = ['spades','hearts','diamonds','clubs']
    values = range(2,11)+['A','J','Q','K']
    deck = list(repeat(list(product(values, suits)),ndecks))
    deck = list(chain(*deck))

    if include_joker:
        deck += [('W','red_joker'), ('W','black_joker')]*ndecks

    return deck

def greeting():
    print '#'*80
    print '{:^80}'.format('CARIOCA')
    print '#'*80

def init_server(server_name='ganymede', port=10000):
    """
    From https://pymotw.com/2/socket/tcp.html
    """
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = (server_name, port)
    print 'Starting up on %s port %s' % server_address
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(5)

    return sock

def interact(msg, *args):
    while 1:
        ans = raw_input(msg)

        if ans in args:
            break
        else:
            print 'Valid options are: ', args

    return ans
   
def interact_size(msg, size, delimiter=','):
    while 1:
        ans = raw_input(msg)
        try:
            ans = map(int, msg.split(delimiter))
        except ValueError:
            print 'Only numbers are accepted, try again'
            continue
        if len(ans)==size:
            break
        else:
            print '%i values must be entered'
    return ans

def sort_cards_key(value):
    return VALUES.keys().index(value)

def get_values_seq():
    # Joker is not included
    return ''.join(map(lambda x: str(x)[0], VALUES.keys()[:-1]))

