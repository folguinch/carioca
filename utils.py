SUITS_UNICODE = {'spades':u'[%s\u2660]', 'hearts':u'[%s\u2665]',
        'diamonds':u'[%s\u2666]', 'stars':u'[%s\u2663]',
        'red_joker':u'[\u2606]', 'black_joker':u'[\u2605]'}

VALUES = dict(zip(range(2,11)+['A','J','Q','K','W'], range(2,11)+[15,10,10,10,30]))

def validate_card(value, suit):
    assert suit in SUITS_UNICODE.keys()
    assert value in VALUES.keys()

    if value=='W' and suit not in ['red_joker','black_joker']:
        raise ValueError('Card value does not match a valid suit')
