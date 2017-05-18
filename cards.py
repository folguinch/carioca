import random, re, pickle
from collections import OrderedDict

from .base import Cards
from .utils import get_values_seq, get_deck

class Deck(Cards):

    def __init__(self, ndecks=2, game=''):
        if game != 'RS':
            cards = get_deck(ndecks)
        else:
            # Do not include the joker in real straight
            cards = get_deck(ndecks, False)
        super(Deck, self).__init__(*cards)

    def shuffle(self):
        random.shuffle(self)

class Discard(list):
    pass

class Hand(Cards):

    def __str__(self):
        fmt = '[{:2}]'
        line1 = '  '.join(map(str,self))
        line2 = '  '.join([fmt.format(i+1) for i in range(len(self))])
        return line1 + '\n' + line2

    def compact(self):
        super(Hand, self).__init__(*filter(lambda x: x is not None, self))

    def unlower(self, cards, low):
        for i, card in zip(cards, low):
            self[i-1] = card

    def lower_three(self, cards):
        low = Down()
        value = None
        wildcards = 0

        # Validate and lower
        for i in cards:
            if self[i-1].value=='W':
                wildcards += 1
                if wildcards > 1:
                    break
                else:
                    low.append(self[i-1])
                    self[i-1] = None
                    continue
            elif value is None:
                value = self[i-1].value
                low.append(self[i-1])
                self[i-1] = None
            elif self[i-1].value == value:
                low.append(self[i-1])
                self[i-1] = None
            else:
                break

        if len(low)==3:
            self.compact()
            return low
        else:
            self.unlower(cards, low)
            return []

    def lower_straight(self, cards):
        assert len(cards) == 4

        # Some deifinitions
        low = Down()
        suit = None
        wildcard = None
        seq = get_values_seq()*2
        regex0 = '.{3}%s.{3}'
        regex1 = '.{0,3}%s.{0,3}'

        # Validate suit and wildcards:
        for i, n in enumerate(cards):
            val = str(self[n].value)[0]
            if val=='W':
                if wildcard is None:
                    wildcard = i
                    low.append(self[n])
                    self[n] = None
                    continue
                else:
                    break
            elif suit is None:
                aux = re.search(regex0 % val, seq)
                seq = aux.group()
                suit = self[n].suit
                low.append(self[n])
                self[n] = None
            elif self[n].suit == suit:
                aux = re.search(regex1 % val, seq)
                if aux is not None:
                    seq = aux.group()
                    low.append(self[n])
                    self[n] = None
                else:
                    break
            else:
                break

        if len(set(low.values))==4:
            if wildcard is None and len(seq)==4:
                self.compact()
                low.sort(pattern=seq)
                return low
            elif len(seq)==5:
                aux = low.pop(wildcard)
                low.sort(pattern=seq)
                if wildcard==0 or wildcard==3:
                    low.insert(wildcard, aux)
                else:
                    low.insert(0, aux)
                self.compact()
                return low
            elif len(seq)==4:
                aux1 = low.pop(wildcard)
                aux2 = ''.join(low.values_as_str())
                aux3 = re.search('[^%s]' % aux2, seq)
                if aux3 is None:
                    raise Exception('Something is wrong')
                low.sort(pattern=seq)
                low.insert(aux3.start(), aux1)
                return low
            else:
                raise Exception('Problems validating straight')
        else:
            self.unlower(cards, low)
            return []

    def get_points(self):
        points = 0
        for card in self:
            points += card.points


class Down(Cards):
    
    def insert_card(self, card, position=None):
        position = self.validate_card(card, position)

        if position is None:
            return False
        else:
            self.insert(position, card)
            return True

    def validate_card(self, card, position=None):
        # Validate the position
        if position is not None:
            if position==-1:
                position = len(self)
            elif position!=0 or position!=len(self):
                position = len(self)
        else:
            position = len(self)

        # Validate card, if position is None card is appended
        if card.value=='W' and 'W' not in self.values:
            return position
        elif card.value=='W':
            i = self.values.index('W')
            if i>4 and len(self)-i>4:
                # Use the given position only if this condition is satisfy
                # otherwise the position should be obvious from each condition
                return position
            elif i>4:
                return 0
            elif len(self)-i>4:
                return len(self)
            else: 
                return None
        elif self.game=='T' and card.value in self.values:
            return position
        elif self.game=='S' and card.suit in self.suits:
            # Given position is irrelevant
            seq = get_values_seq()*2
            ab = str(card.value)[0] + str(self[0].value)[0]
            ba = str(self[-1].value)[0] + str(card.value)[0]
            if ab in seq:
                return 0
            elif ba in seq:
                return len(self)
            else:
                return None
        else:
            return None

class Table:
    def __init__(self, names):
        self.table = OrderedDict.fromkeys(names)

    def __setitem__(self, key, val):
        self.table[key] = val

    def __getitem__(self, key):
        return self.table[key]

    def __str__(self):
        lines = ''
        fmt = '[%i] %s: \n%s'
        for i,(name, down) in enumerate(self.table.items()):
            if down is not None:
                fmt2 = '\t[%i] %s\n'
                cards = ''
                for j,d in enumerate(down):
                    cards += fmt2 % (j+1, d)
            else:
                cards = '\t-----'

            lines += fmt % (i+1, name, cards)
        return lines.strip()

    def __iter__(self):
        for key in self.table.keys():
            if self.table[key] is not None:
                yield key

    def reset(self, name):
        self.table[name] = None

    def encode(self):
        return pickle.dumps(self)

    def append(self, key, value):
        if self.table[key] is None:
            self.table[key] = []
        self.table[key] += [value]

    def insert_card(self, name, card):
        assert self.table[name] is not None

        return self.table[name].insert_card(card)

    def is_empty(self):
        aux = True
        for i in self.table.values():
            if i is not None:
                aux = False
                break
        return aux
