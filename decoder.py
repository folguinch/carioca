import cPickle as pickle

from .base import Card, Cards
from .cards import Table, Hand, Down

def decode_msg(load):
    return pickle.loads(load)
