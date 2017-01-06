from itertools import product, repeat, chain

SUITS_UNICODE = {'spades':u'[%s\u2660]', 'hearts':u'[%s\u2665]',
        'diamonds':u'[%s\u2666]', 'clubs':u'[%s\u2663]',
        'red_joker':u'[\u2606]', 'black_joker':u'[\u2605]'}

VALUES = dict(zip(range(2,11)+['A','J','Q','K','W'], range(2,11)+[15,10,10,10,30]))

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
    suits = ['spades','hearts','diamonds','stars']
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
