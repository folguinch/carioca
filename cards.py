import random

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

    def compact(self):
        self = filter(lambda x: x is not None, self)

    def unlower(self, cards, low):
        for i, card in zip(cards, low):
            self[i] = card

    def lower_three(self, cards):
        low = Down()
        value = None
        wildcards = 0

        # Validate and lower
        for i in cards:
            if self[i].value=='W':
                wildcards += 1
                if wildcards > 1:
                    break
                else:
                    low.append(self[i])
                    self[i] = None
                    continue
            elif value is None:
                value = self[i].value
                low.append(self[i])
                self[i] = None
            elif self[i].value == value:
                low.append(self[i])
                self[i] = None
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


    #def __init__(self, cards, nmax=12):
    #    self.nmax = nmax
    #    super(Hand, self).__init__(*cards)

class Down(Cards):
    pass

